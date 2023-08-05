# This file is part of Sympathy for Data.
# Copyright (c) 2013 Combine Control Systems AB
#
# Sympathy for Data is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# Sympathy for Data is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Sympathy for Data.  If not, see <http://www.gnu.org/licenses/>.
import os
import functools
import logging

import Qt.QtCore as QtCore
import Qt.QtWidgets as QtWidgets

import sympathy.platform.exceptions as platform_exc
from sympathy.platform import version_support as vs
from sympathy.platform import os_support as oss

from . import flow
from . windows import flow_window
from . import settings
from . import common
from . import signals
from . import user_statistics

core_logger = logging.getLogger('core')


class GuiManager(QtCore.QObject):
    """
    Mediator between flows, flow windows and main window.
    """

    def __init__(self, main_window, app_core, parent=None):
        super(GuiManager, self).__init__(parent)
        self._main_window = main_window
        self._app_core = app_core
        self._flows = []
        self._flow_windows = {}
        self._flow_counter = 0
        self._signals = signals.SignalHandler()
        self._main_window.new_flow.connect(self.create_flow)
        self._main_window.open_flow[str].connect(self.open_flow)
        self._main_window.open_named_flow[str].connect(
            self.open_flow_from_file)
        self._main_window.open_flow_window.connect(self._open_flow_window)
        self._init()

    def _init(self):
        # Restore session
        settings_ = settings.instance()
        if settings_['Gui/on_start'] == settings.on_start_last_session:
            files = settings_['session_files']
            for file_ in files:
                if os.path.exists(file_):
                    QtCore.QTimer.singleShot(
                        0, functools.partial(
                            self.open_flow_from_file, file_))

    @QtCore.Slot()
    def create_flow(self, flow_uuid=None):
        """Create a new flow."""
        if (settings.instance()['Gui/on_start'] != settings.on_start_new_flow and
                self._flow_counter == 0):
            self._flow_counter += 1
            return
        flow_ = self._app_core.create_flow(flow_uuid)
        flow_.unsaved_name = 'New Flow {}'.format(self._flow_counter)
        self._flow_counter += 1
        self._flows.append(flow_)
        self._open_flow_window(flow_)
        return flow_

    @QtCore.Slot(flow.Flow)
    def _open_flow_window(self, flow_):
        """Bring forth or create a flow window."""
        if flow_ in self._flow_windows:
            self._main_window.show_flow(flow_)
        else:
            flow_window_ = flow_window.FlowWindow(
                flow_, self, self._app_core, parent=self._main_window)
            self._flow_windows[flow_] = flow_window_
            self._main_window.add_flow_window(flow_window_)
            self._signals.connect_reference(flow_, [
                (flow_window_.new_signal, self.create_flow),
                (flow_window_.edit_subflow_requested[flow.Flow],
                 self._open_flow_window),
                (flow_window_.help_requested[str],
                 self._main_window.open_documentation),
                (flow_.name_changed[str],
                 functools.partial(
                    lambda x:
                     self._main_window.handle_flow_name_changed(flow_)))])

    def _abort_root_flow(self, flow_):
        if flow_.is_root_flow():
            # Parent flow. Shut down any pending executing on flow.
            flow_.abort()

    def _close_flow(self, flow_):
        """Close and delete flow"""
        self._signals.disconnect_all(flow_)
        if flow_ in self._flows:
            self._main_window.close_flow_window(self._flow_windows[flow_])
            del self._flows[self._flows.index(flow_)]
            del self._flow_windows[flow_]
        elif flow_ in self._flow_windows:
            self._main_window.close_flow_window(self._flow_windows[flow_])
            del self._flow_windows[flow_]

    def close_tree(self, flow_, force):
        cancelled = False
        if flow_ in self._flows:
            cancelled = False
            if settings.instance()['ask_for_save']:
                try:
                    common.ask_about_saving_flows(
                        [flow_], include_root=True, discard=True)
                except common.SaveCancelled:
                    cancelled = True

        if not cancelled:
            self._abort_root_flow(flow_)
            user_statistics.user_closed_workflow(flow_)
            self._close_flow(flow_)

            if force or flow_.is_root_flow():
                for flow_ in reversed(flow_.all_subflows()):
                    if flow_ in self._flow_windows:
                        self._main_window.close_flow_window(
                            self._flow_windows[flow_])
                        del self._flow_windows[flow_]

    def save_as_flow(self, flow_):
        """Save flow with a new file name."""
        flow_to_save = flow_.root_or_linked_flow()
        flow_to_save.save(True)
        self._main_window.handle_flow_name_changed(flow_to_save)

    def save_flow(self, flow_, propagate_cancelled=False):
        """Save flow, if no filename exists, prompt."""
        flow_to_save = flow_.root_or_linked_flow()
        prompt = flow_to_save.filename == ''
        try:
            flow_to_save.save(prompt, propagate_cancelled=propagate_cancelled)
        except common.SaveCancelled:
            if propagate_cancelled:
                raise

    @QtCore.Slot(str)
    def open_flow(self, default_directory):
        """Open a flow (with dialog)"""
        if default_directory == '':
            default_directory = settings.instance()['default_folder']
        result = QtWidgets.QFileDialog.getOpenFileNames(
            None, 'Open flow', default_directory, 'Sympathy flow (*.syx)')
        if isinstance(result, tuple):
            filenames = result[0]
        else:
            filenames = result
        for filename in filenames:
            self.open_flow_from_file(filename)

    @QtCore.Slot(str)
    def open_flow_from_file(self, filename):
        """Open flow with given file name."""
        filename = vs.fs_decode(filename)
        scratch_flow = self._main_window.get_scratch_flow()
        scratch_clean = False
        if scratch_flow and scratch_flow.subflows_are_clean():
            scratch_clean = True
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        error, details = "", ""
        try:
            common.add_flow_to_recent_flows_list(os.path.abspath(filename))
            new_flow = common.read_flow_from_file(
                self._app_core, filename, self._flows, self._open_flow_window)
            new_flow.validate()
            if scratch_flow and scratch_clean:
                self._close_flow(scratch_flow)
        except platform_exc.ReadSyxFileError as e:
            error = e.cause
            details = e.details
        except platform_exc.ConflictingGlobalLibrariesError as e:
            msg_box = QtWidgets.QMessageBox(
                QtWidgets.QMessageBox.Warning, u"Sympathy for Data",
                "Flow libraries of {} are in conflict with global libraries: "
                "{}.\n\nRemove conflicting global libraries and reopen the "
                "flow."
                .format(
                    os.path.basename(filename),
                    ', '.join(e.libs)),
                QtWidgets.QMessageBox.Ok,
                self._main_window)
            msg_box.setInformativeText(error)
            msg_box.setDetailedText(details)
            msg_box.exec_()

        except platform_exc.ConflictingFlowLibrariesError:
            msg_box = QtWidgets.QMessageBox(
                QtWidgets.QMessageBox.Warning, u"Sympathy for Data",
                "Flow libraries of {} are in conflict with libraries from "
                "flows that are already open."
                "\n\nOpen in a new Sympathy instance?"
                .format(
                    os.path.basename(filename)),
                QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel,
                self._main_window)
            msg_box.setInformativeText(error)
            msg_box.setDetailedText(details)
            res = msg_box.exec_()
            if res == QtWidgets.QMessageBox.Ok:
                oss.open_in_new_sympathy(filename)
            # else:
            #     new_flow = common.read_flow_from_file(
            #         self._app_core, filename, self._flows,
            #         self._open_flow_window,
            #         warn_on_errors=[
            #             platform_exc.ConflictingFlowLibrariesError])

        finally:
            QtWidgets.QApplication.restoreOverrideCursor()
        if error:
            msg_box = QtWidgets.QMessageBox(
                QtWidgets.QMessageBox.Warning, u"Sympathy for Data",
                u"Couldn't open flow {}.".format(
                    os.path.basename(filename)),
                QtWidgets.QMessageBox.Ok, self._main_window)
            msg_box.setInformativeText(error)
            msg_box.setDetailedText(details)
            msg_box.exec_()

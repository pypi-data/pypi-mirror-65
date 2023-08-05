# This file is part of Sympathy for Data.
# Copyright (c) 2018 Combine Control Systems AB
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
from Qt import QtCore
from Qt import QtGui
from Qt import QtWidgets
import datetime
import logging
import os
import sys
import re
import weakref
from collections import OrderedDict

from sympathy.platform import widget_library as sywidgets
from sympathy.platform import node_result
from sympathy.utils import prim

from .. import util
from .. import flow
from .. import common
from .. import themes
from . import issues
from .. import settings

import sympathy.app.library


core_logger = logging.getLogger('core')

(level_role,
 node_role,
 brief_role,
 details_role,
 stream_ident_role,
 stream_data_role) = range(QtCore.Qt.UserRole, QtCore.Qt.UserRole + 6)


def icon_path(icon):
    """Return icon path for icon"""
    return os.path.join(util.icon_path('actions'), icon)


class IndirectNode(object):
    """
    Workaround wrapper to make Lambda supported by
    QListWidgetItem.setData.
    """

    def __init__(self, node):
        if node is not None:
            self._node_ref = weakref.ref(node)
        else:
            self._node_ref = None

    @property
    def node(self):
        if self._node_ref is None:
            return None
        else:
            return self._node_ref()


class IndirectList(object):
    def __init__(self, list):
        self.list = list


class MessageView(QtWidgets.QListWidget):
    """Shows errors and output"""

    goto_node_requested = QtCore.Signal(flow.Node)

    colors = OrderedDict([
        ('Exception', QtGui.QColor.fromRgb(128, 49, 55, 255)),
        ('Error', QtGui.QColor.fromRgb(128, 49, 55, 255)),
        ('Warnings', QtGui.QColor.fromRgb(253, 182, 0, 255)),
        ('Notice', QtGui.QColor.fromRgb(0, 100, 0, 255))])
    icons = {
        'Exception': util.icon_path('node_error.svg'),
        'Error': util.icon_path('node_error.svg'),
        'Warnings': util.icon_path('node_warning.svg'),
        'Notice': util.icon_path('node_executed.svg')}

    def __init__(self, app_core, font, parent=None):
        super().__init__(parent)
        self._stream_item_cache = {}
        self._app_core = app_core
        self.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self._font = font
        self._context_menu = QtWidgets.QMenu(parent=self)
        self._goto_selected_action = QtWidgets.QAction('Go to Node', self)

        theme = themes.get_active_theme()
        self._report_issue_action = QtWidgets.QAction(
            QtGui.QIcon(theme.report_issue), 'Report Issue', self)
        self._goto_selected_action.triggered.connect(self._handle_goto_node)
        self._report_issue_action.triggered.connect(self._handle_report_issue)
        self._context_menu.addAction(self._goto_selected_action)

        icon = QtGui.QIcon(icon_path(theme.delete))
        self._remove_selected = QtWidgets.QAction(
            icon, 'Remove selected', self)
        self._remove_selected.triggered.connect(self.clear_selected)
        self._context_menu.addAction(self._remove_selected)
        self.clear_action = QtWidgets.QAction(icon, 'Clear All', self)
        self.clear_action.setToolTip('Clear the entire Messages log')
        self.clear_action.triggered.connect(self.clear)
        self._context_menu.addAction(self.clear_action)
        self._context_menu.addSeparator()
        self._context_menu.addAction(self._report_issue_action)

        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        policy = self.sizePolicy()
        policy.setHorizontalPolicy(policy.Minimum)
        self.setSizePolicy(policy)

        self._goto_selected_action.triggered.connect(self._handle_goto_node)

    def _handle_goto_node(self):
        selected_items = self.selectedItems()
        for item in selected_items:
            node = item.data(node_role).node
            if node:
                self.goto_node_requested.emit(node)

    def _anonymize_traceback(self, string):
        """
        Attempt to cleanup identifying traceback information in File
        paths.
        """
        lines = []
        for line in string.splitlines():
            match = re.match('^(.*)File "([^"]*)"(.*)$', line)
            if match:
                prefix, file_, suffix = match.groups()
                replaced = False
                for name, path in [
                        ('sympathy', prim.sympathy_path()),
                        ('sylib', prim.sylib_path()),
                        ('python_prefix', sys.prefix),
                        ('python_exec_prefix', sys.exec_prefix)]:

                    if file_.startswith(path):
                        file_ = file_.replace(path, name, 1)
                        replaced = True
                        break
                if replaced:
                    lines.append(f'{prefix}File "{file_}"{suffix}')
                else:
                    lines.append(f'{prefix}File "omitted"{suffix}')
            else:
                lines.append(line)
        return '\n'.join(lines)

    def _handle_report_issue(self):

        selected_items = self.selectedItems()
        for item in selected_items:
            node = item.data(node_role).node

            level = item.data(level_role)
            description = MessageDetails.item_text(item)
            generated = True

            if level == 'Exception':
                # Attempt to cleanup identifying traceback information.
                description = self._anonymize_traceback(description)

            if not level:
                level = 'behavior'

            subject = 'Unexpected {level} in {node} node'.format(
                level=level.lower(),
                node=node.library_node_name)
            dialog = issues.IssueReportSender(
                subject=subject, details=description, generated=generated)

            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                pass

    def _get_item(self, parent, messages):
        item = QtWidgets.QListWidgetItem(messages[0], parent)
        item.setFont(self._font)
        return item

    def clear(self):
        self._stream_item_cache.clear()
        super().clear()

    def clear_selected(self):
        selected_indices = self.selectedIndexes()
        model = self.model()
        for index in selected_indices:
            item = self.itemFromIndex(index)
            ident = item.data(stream_ident_role)
            if ident is not None:
                self._stream_item_cache.pop(ident, None)

            if index.column() > 0:
                continue
            model.removeRow(index.row())

    def _cleanup(self, s):
        return s.replace('\n', ' ').replace('\r', ' ').replace(
            '\t', ' ').strip()

    def _clean_node_and_name(self, identifier):
        try:
            node = self._app_core.get_flode(identifier)
            name = node.name
        except (KeyError, AttributeError, ValueError):
            node = None
            name = identifier
        return node, self._cleanup(name)

    @QtCore.Slot(str, object)
    def add_node_output_message(self, full_uuid, output):
        if not (output.stderr or output.stdout or output.has_exception()):
            return

        node, name = self._clean_node_and_name(full_uuid)

        levels = {}
        if output.has_exception():
            key, details = common.format_output_exception(output)
            levels[key] = (self._cleanup(output.exception.string), details)
        stderr = output.stderr
        if stderr:
            if not output.stderr_clean:
                stderr = self._cleanup(stderr)
            levels['Warnings'] = (stderr, '')
        stdout = output.stdout
        if stdout:
            if not output.stdout_clean:
                stdout = self._cleanup(stdout)
            levels['Notice'] = (stdout, '')

        for key, (brief, details) in levels.items():
            parent = QtWidgets.QListWidgetItem(name, None)
            indirect_node = IndirectNode(node)
            parent.setIcon(QtGui.QIcon(self.icons[key]))
            parent.setForeground(QtGui.QBrush(self.colors[key]))
            parent.setData(node_role, indirect_node)
            parent.setData(QtCore.Qt.ToolTipRole, str(
                datetime.datetime.now().isoformat()))

            parent.setData(level_role, key)

            if brief:
                parent.setData(brief_role, brief)

            if details:
                parent.setData(details_role, details)

            if node:
                parent.setData(node_role, indirect_node)
            self.addItem(parent)

        self.scrollToBottom()

    @QtCore.Slot(int, object)
    def add_node_output_stream_message(self, taskid, ident, kind, output):

        def cleanup(s):
            return s.replace('\n', ' ').replace('\r', ' ').replace(
                '\t', ' ').strip()

        key = (taskid, ident, kind)

        node, name = self._clean_node_and_name(ident)
        item = self._stream_item_cache.get(key)
        if item is None:
            item = QtWidgets.QListWidgetItem(name, None)
            indirect_node = IndirectNode(node)
            item.setIcon(QtGui.QIcon(self.icons[kind]))
            item.setForeground(QtGui.QBrush(self.colors[kind]))
            item.setData(node_role, indirect_node)
            item.setData(QtCore.Qt.ToolTipRole, str(
                datetime.datetime.now().isoformat()))
            item.setData(node_role, indirect_node)
            self.addItem(item)
            self.scrollToBottom()
            data = IndirectList([])
            item.setData(stream_ident_role, key)
            item.setData(stream_data_role, data)
        else:
            data = item.data(stream_data_role)
            if data is None:
                data = IndirectList([])
                item.setData(stream_ident_role, key)
                item.setData(stream_data_role, data)

        data.list.append(output)
        self._stream_item_cache[key] = item

    def contextMenuEvent(self, event):
        selected_items = self.selectedItems()
        platform_node = False
        for item in selected_items:
            node = item.data(node_role).node
            platform_node = False
            if node:
                platform_node = sympathy.app.library.is_platform_node(node.library_node)

        self._report_issue_action.setEnabled(platform_node)
        self._context_menu.exec_(event.globalPos())
        super().contextMenuEvent(event)


class MessageDetails(QtWidgets.QTextEdit):

    def __init__(self, font, parent=None):
        super().__init__(parent=parent)
        self._font = font
        self.setFont(self._font)
        self._key = None
        text_interaction_flags = (QtCore.Qt.TextSelectableByMouse |
                                  QtCore.Qt.TextSelectableByKeyboard)
        # TODO: Editable on Mac to workaround a Qt bug that otherwise results
        # in non-working keyboard shortcuts for Copy and Select all actions.
        if sys.platform == 'darwin':
            text_interaction_flags |= QtCore.Qt.TextEditable

        self.setTextInteractionFlags(text_interaction_flags)

    @staticmethod
    def item_text(item):
        stream_data = item.data(stream_data_role)
        if stream_data is not None:
            stream_data = stream_data.list
        else:
            stream_data = []
        res = ''
        if stream_data:
            res = ''.join(stream_data)
        else:
            brief = item.data(brief_role)
            details = item.data(details_role)

            if brief and details:
                res = '\n\n'.join([brief, details])
            elif brief:
                res = brief
            elif details:
                res = details
        return res

    def set_current_items(self, items):
        self.clear()
        for item in items:
            self.setPlainText(self.item_text(item))
            self._key = item.data(stream_ident_role)

    def add_node_output_stream_message(self, taskid, ident, kind, output):
        key = (taskid, ident, kind)
        if self._key is not None and self._key == key:
            vscrollbar = self.verticalScrollBar()
            vscroll = vscrollbar.value()
            textcursor = self.textCursor()
            cursor_start = textcursor.selectionStart()
            cursor_end = textcursor.selectionEnd()
            self.moveCursor(QtGui.QTextCursor.End)
            self.insertPlainText(output)
            textcursor = self.textCursor()
            textcursor.setPosition(cursor_start)
            textcursor.setPosition(cursor_end, QtGui.QTextCursor.KeepAnchor)
            self.setTextCursor(textcursor)
            vscrollbar.setValue(vscroll)


class MessageWidget(QtWidgets.QWidget):
    """Shows the errors and outputs togheter with a toolbar."""

    goto_node_requested = QtCore.Signal(flow.Node)

    def __init__(self, app_core, parent=None):
        super().__init__(parent=parent)
        self._app_core = app_core
        self._init_gui()
        self._tasks = set()

    def _init_gui(self):
        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self._font = QtGui.QFont('Courier')

        self._message_view = MessageView(
            self._app_core, self._font)
        self._message_view.goto_node_requested.connect(
            self.goto_node_requested)
        self._message_details = MessageDetails(self._font)

        self._message_view.itemSelectionChanged.connect(
            self._selected_items_changed)

        self._message_view.clear_action.triggered.connect(
            self._message_details.clear)

        self._toolbar = sywidgets.SyBaseToolBar(parent=self)
        self._toolbar.setOrientation(QtCore.Qt.Vertical)
        self._toolbar.setIconSize(QtCore.QSize(16, 16))
        self._toolbar.addAction(self._message_view.clear_action)

        splitter = QtWidgets.QSplitter()
        splitter.addWidget(self._message_view)
        splitter.addWidget(self._message_details)

        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)

        layout.addWidget(self._toolbar)
        layout.addWidget(splitter)
        self.setLayout(layout)

    @QtCore.Slot(str, dict)
    def add_node_output_message(self, full_uuid, output):
        self._message_view.add_node_output_message(full_uuid, output)

    def add_node_output_stream_message(self, taskid, ident, kind, text):
        self._message_details.add_node_output_stream_message(
            taskid, ident, kind, text)
        self._message_view.add_node_output_stream_message(
            taskid, ident, kind, text)

    @QtCore.Slot(str, str)
    def add_message(self, full_uuid, message):
        result = node_result.NodeResult()
        result.stdout = message
        result.stderr_clean = True
        self._message_view.add_node_output_message(full_uuid, result)

    def _selected_items_changed(self):
        self._message_details.set_current_items(
            self._message_view.selectedItems())

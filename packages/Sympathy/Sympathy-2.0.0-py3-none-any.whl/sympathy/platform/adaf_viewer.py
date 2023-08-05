# This file is part of Sympathy for Data.
# Copyright (c) 2013, Combine Control Systems AB
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
import re



from Qt import QtCore, QtWidgets

from .viewerbase import ViewerBase
from .table_viewer import TableViewer


def combined(string):
    def to_int(string):
        try:
            return int(string)
        except ValueError:
            return string
    return [to_int(part) for part in re.split('([0-9]+)', string)]


class ADAFViewer(ViewerBase):
    def __init__(self, adaf_data=None, console=None, parent=None):
        super(ADAFViewer, self).__init__(parent)

        self._adaf = adaf_data
        self._meta_table = None
        self._result_table = None

        self._init_gui()

        self.update_data(adaf_data)

    def adaf(self):
        return self._adaf

    def data(self):
        return self.adaf()

    def _update_rasters(self, rasters, name):
        self._raster_combowidget.clear()
        self._raster_combowidget.addItems(rasters)

        if name in rasters:
            self._raster_combowidget.setCurrentIndex(
                self._raster_combowidget.findText(
                    name,
                    QtCore.Qt.MatchExactly))
        elif len(rasters):
            self._raster_combowidget.setCurrentIndex(0)

    def update_data(self, adaf_data):

        if adaf_data is not None:
            self._adaf = adaf_data
            self._meta_table = self._adaf.meta.to_table()
            self._meta_table.set_name('Meta')
            self._meta_viewer.update_data(self._meta_table)

            self._result_table = self._adaf.res.to_table()
            self._result_table.set_name('Result')
            self._result_viewer.update_data(self._result_table)

            prev_system_name = str(
                self._system_combowidget.currentText())
            prev_raster_name = str(
                self._raster_combowidget.currentText())

            systems = [self._system_combowidget.itemText(i)
                       for i in range(self._system_combowidget.count())]

            rasters = [self._raster_combowidget.itemText(i)
                       for i in range(self._raster_combowidget.count())]

            new_systems = sorted(adaf_data.sys.keys(), key=combined)
            try:
                prev_system = adaf_data.sys[prev_system_name]
            except KeyError:
                system_names = adaf_data.sys.keys()
                if len(system_names):
                    prev_system = adaf_data.sys[system_names[0]]
                else:
                    self._system_combowidget.clear()
                    self._raster_combowidget.clear()
                    self._raster_viewer.clear()
                    return

            new_rasters = sorted(prev_system.keys(), key=combined)

            if systems != new_systems:
                self._raster_viewer.clear()
                self._system_combowidget.clear()
                self._system_combowidget.addItems(new_systems)

                if prev_system_name in new_systems:
                    self._system_combowidget.setCurrentIndex(
                        self._system_combowidget.findText(
                            prev_system_name,
                            QtCore.Qt.MatchExactly))

                    if rasters != new_rasters:
                        self._update_rasters(new_rasters, prev_raster_name)

            elif rasters != new_rasters:
                self._raster_viewer.clear()
                self._update_rasters(new_rasters, prev_raster_name)

            self._change_raster_using_system(
                self._raster_combowidget.currentText(),
                self._system_combowidget.currentText())

    def _init_gui(self):
        layout = QtWidgets.QVBoxLayout()

        tabwidget = QtWidgets.QTabWidget()

        self._meta_viewer = TableViewer(
            self._meta_table, show_title=False, plot=False)
        tabwidget.addTab(self._meta_viewer, 'Meta')

        self._result_viewer = TableViewer(
            self._result_table, show_title=False, plot=False)
        tabwidget.addTab(self._result_viewer, 'Result')

        self._system_combowidget = QtWidgets.QComboBox()
        self._raster_combowidget = QtWidgets.QComboBox()

        system_layout = QtWidgets.QHBoxLayout()
        system_layout.setContentsMargins(11, 2, 11, 0)
        system_layout.addWidget(QtWidgets.QLabel('System:'))
        system_layout.addWidget(self._system_combowidget)
        system_layout.addWidget(QtWidgets.QLabel('Raster:'))
        system_layout.addWidget(self._raster_combowidget)
        system_layout.addStretch()
        # wrap it in a widget, so it gets aligned with the table viewer
        system_widget = QtWidgets.QWidget()
        policy = QtWidgets.QSizePolicy()
        policy.setHorizontalStretch(0)
        system_widget.setSizePolicy(policy)
        system_widget.setLayout(system_layout)

        self._raster_viewer = TableViewer(plot=True, show_title=False)

        timeseries_layout = QtWidgets.QVBoxLayout()
        timeseries_layout.setContentsMargins(5, 5, 5, 5)
        timeseries_layout.setSpacing(0)
        timeseries_layout.addWidget(system_widget)
        timeseries_layout.addWidget(self._raster_viewer)

        timeseries_widget = QtWidgets.QWidget()
        timeseries_widget.setLayout(timeseries_layout)
        tabwidget.addTab(timeseries_widget, 'Timeseries')

        layout.addWidget(tabwidget)

        self.setLayout(layout)

        self._system_combowidget.currentIndexChanged[int].connect(
            self._system_changed)
        self._raster_combowidget.currentIndexChanged[int].connect(
            self._raster_changed)

    def _system_changed(self, system_idx):
        system_name = self._system_combowidget.currentText()
        if system_name not in self._adaf.sys.keys():
            return
        rasters = self._adaf.sys[system_name].keys()

        try:
            prev_raster_name = str(
                self._raster_combowidget.currentText())
        except AttributeError:
            prev_raster_name = None

        self._update_rasters(rasters, prev_raster_name)

    def _change_raster_using_system(self, raster_name, system_name):
        if not raster_name or not system_name:
            self._raster_viewer.clear()
        else:
            raster = self._adaf.sys[system_name][raster_name]
            raster_table = raster.to_table('({})'.format(raster_name))
            raster_table.set_name(raster_name)
            self._raster_viewer.update_data(raster_table)

    def _raster_changed(self, raster_idx):
        raster_name = self._raster_combowidget.currentText()
        system_name = self._system_combowidget.currentText()
        current_system_idx = self._system_combowidget.currentIndex()
        if current_system_idx is None:
            return
        self._change_raster_using_system(
            str(raster_name), system_name)

    def custom_menu_items(self):
        return []

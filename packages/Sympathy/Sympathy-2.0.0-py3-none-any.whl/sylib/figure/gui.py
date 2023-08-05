# This file is part of Sympathy for Data.
# Copyright (c) 2016, Combine Control Systems AB
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
import json
import uuid
import functools
import itertools

from sympathy.api import qt2 as qt
from sympathy.api import ParameterView, node as synode
from sympathy.platform.widget_library import SyBaseToolBar
from sylib.figure import models
from sylib.icons import utils as icon_utils
from sylib.tree_model import qt_model, models as base_models

QtCore = qt.QtCore
QtGui = qt.QtGui
QtWidgets = qt.QtWidgets

MIME = {
    'layout_tree_item_id': 'application-x-sympathy/figure.layout.tree.item.id',
    'layout_tree_new_item':
        'application-x-sympathy/figure.layout.tree.new.item',
    'instance': 'application-x-sympathy/figure.instance'
}


TOOLBAR_ITEMS = [
    'separator',
    models.Axes,
    'separator',
    models.LinePlot,
    models.ScatterPlot,
    models.BarPlot,
    models.HistogramPlot,
    models.TimelinePlot,
    models.HeatmapPlot,
    models.BoxPlot,
    models.PieChart,
    models.Annotation,
    'separator',
    models.BarContainer,
    models.Iterator,
    'separator',
    models.Legend,
    models.Grid,
]


ITEM_TYPE_TO_CLASS = {
    i.node_type: i for i in TOOLBAR_ITEMS if i != 'separator'}


class Names:
    """
    Helper class to manage and provide names to the wizard methods.
    """

    def __init__(self, data):
        self._data = data

        fields = ['expr', 'path', 'name']
        names = list(data.names(kind='cols', fields=fields))
        self._expr = [f"arg{n.get('expr', '')}" for n in names]
        self._path = [n.get('path', []) for n in names]
        self._name = [n.get('name', '') for n in names]

        self._opts = self._uniquify([self._path_join(p) for p in self._path])
        self._opts_lookup = {v: i for i, v in enumerate(self._opts)}

    def _uniquify(self, opts):
        res = []
        out = set(opts)
        cnt = {}
        for k in opts:
            cnt[k] = opts.count(k)

        for k in opts:
            if cnt[k] == 1:
                res.append(k)
            else:
                for i in itertools.count():
                    candidate = f'{k}:{i}'
                    if candidate not in out:
                        res.append(candidate)
                        break
        return res

    def _path_join(self, path):
        return '/'.join(
            [str(seg[-1]) for seg in path if seg and seg[-1] != []])

    @property
    def options(self):
        return self._opts

    def to_name(self, option):
        try:
            return self._name[self._opts_lookup[option]]
        except KeyError:
            return ''

    def to_expr(self, option):
        try:
            return self._expr[self._opts_lookup[option]]
        except KeyError:
            return ''


class Wizard(QtCore.QObject):
    """
    Inherit this class to create another Figure wizard.

    Always override:
        * name
        * description
        * _init_parameters
        * _get_model
    Optionally override:
        * _adjust_parameters
    """
    wizard_changed = QtCore.Signal()

    name = None
    description = None

    def __init__(self, model):
        super().__init__()
        self._model = model
        self._parameters = synode.parameters()
        self._init_parameters(self._parameters)

        self._data_names = Names(self._model.get_data_table())
        self._adjust_parameters(self._parameters, self._data_names)

        self._parameters.value_changed.add_handler(self._params_changed)

    def gui(self):
        """
        Return a gui for the wizard, with a title, help text and all
        parameters.
        """
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel(
            "<h1>{} plot</h1>".format(self.name.capitalize())))
        layout.addWidget(self._parameters.gui())
        widget.setLayout(layout)
        return widget

    def get_model(self):
        return self._get_model(self._parameters, self._data_names)

    def _params_changed(self):
        self.wizard_changed.emit()

    def _init_parameters(self, parameters):
        """
        Override to create parameter structure in parameters argument using
        parameter helper.
        """
        raise NotImplementedError()

    def _adjust_parameters(self, parameters, names):
        """Override to adjust the parameters to the input data table."""
        pass

    def _get_model(self, parameters, names):
        """
        Override to specify how the figure model should be created from the
        parameters.
        """
        raise NotImplementedError()


class ScatterWizard(Wizard):
    name = 'scatter'
    description = ("Scatter plot, optionally using "
                   "extra signals for color/size.")

    def _init_parameters(self, parameters):
        parameters.set_string(
            'x_signal', label='X signal',
            description='A signal with the x coordinates of all points.',
            editor=synode.editors.combo_editor(filter=True))
        parameters.set_string(
            'y_signal', label='Y signal',
            description='A signal with the y coordinates of all points.',
            editor=synode.editors.combo_editor())
        parameters.set_string(
            'colors', label='Color signal (optional)',
            description='A signal which should be used to determine '
                        'the color of each point.',
            editor=synode.editors.combo_editor(include_empty=True))
        parameters.set_string(
            'sizes', label='Size signal (optional)',
            description='A signal which should be used to determine '
                        'the size of each point.',
            editor=synode.editors.combo_editor(include_empty=True))
        parameters.set_integer(
            'size_scale', value=100, label='Size scale factor',
            description='A factor which is multiplied with all sizes in '
                        'the size signal.')

    def _adjust_parameters(self, parameters, names):
        parameters['x_signal'].adjust(names.options)
        parameters['y_signal'].adjust(names.options)
        parameters['colors'].adjust(names.options)
        parameters['sizes'].adjust(names.options)

    def _get_model(self, parameters, names):
        x_sig = parameters['x_signal'].value
        y_sig = parameters['y_signal'].value
        col_sig = parameters['colors'].value
        size_sig = parameters['sizes'].value
        scale = parameters['size_scale'].value
        plot = {
            "xdata": (names.to_expr(x_sig), "py"),
            "ydata": (names.to_expr(y_sig), "py"),
            "edgecolors": ("#000000", "value"),
            "linewidths": ("0.2", "value"),
            "type": "scatter"
        }
        if col_sig:
            plot["color"] = (names.to_expr(col_sig), "py")
            plot["colorbar"] = {
                "show": ("True", "value"),
                "label": (names.to_name(col_sig), "value"),
            }
        title_postfix = ""
        if size_sig:
            plot["s"] = (f"{scale}*{names.to_expr(size_sig)}", "py")
            title_postfix = f" (size = {names.to_name(size_sig)})"
        else:
            plot["s"] = (f"{scale}".format(scale), "value")

        x_sig_name = names.to_name(x_sig)
        y_sig_name = names.to_name(y_sig)
        return {
            "axes": [{
                "title": (
                    f"{x_sig_name} vs. {y_sig_name}{title_postfix}", "value"),
                "xaxis": {
                    "position": ("bottom", "value"),
                    "label": (x_sig_name, "value")
                },
                "yaxis": {
                    "position": ("left", "value"),
                    "label": (y_sig_name, "value")
                },
                "plots": [plot]
            }]}


class LineWizard(Wizard):
    name = 'line'
    description = "Line plot with one or more signals."

    def _init_parameters(self, parameters):
        parameters.set_string(
            'title', label='Title',
            description='The title for the plot.')
        parameters.set_string(
            'y_label', label='Y Label',
            description='A label for the Y axis.')
        parameters.set_string(
            'x_signal', label='X Signal',
            description='Select the signal that defines the x axis '
                        '(e.g. time).',
            editor=synode.editors.combo_editor(filter=True))
        parameters.set_list(
            'y_signals', label='Y Signals',
            description='Check any signals which should be plotted. '
                        'Each checked signal gets its own color.',
            editor=synode.editors.multilist_editor(mode=False))
        parameters.set_boolean(
            'markers', value=False, label='Mark data points',
            description='Mark each data point with a circle.')

    def _adjust_parameters(self, parameters, names):
        parameters['x_signal'].adjust(names.options)
        parameters['y_signals'].adjust(names.options)

    def _get_model(self, parameters, names):
        title = parameters['title'].value
        x_sig = parameters['x_signal'].value
        y_sigs = parameters['y_signals'].value_names
        y_label = parameters['y_label'].value
        markers = parameters['markers'].value
        plots = [
            {
                "xdata": (names.to_expr(x_sig), "py"),
                "ydata": (names.to_expr(y_sig), "py"),
                "label": (names.to_name(y_sig), "value"),
                "type": "line"
            }
            for y_sig in y_sigs
        ]
        if markers:
            for plot in plots:
                plot['marker'] = ("circle", "value")
        return {
            "axes": [{
                "title": (title, "value"),
                "xaxis": {
                    "position": ("bottom", "value"),
                    "label": (names.to_name(x_sig), "value")
                },
                "yaxis": {
                    "position": ("left", "value"),
                    "label": (y_label, "value")
                },
                "plots": plots,
                "legend": {
                    "show": ("True", "value"),
                }
            }]}


class BarWizard(Wizard):
    name = 'bar'
    description = "Grouped bar plot of one or more signals."

    def _init_parameters(self, parameters):
        parameters.set_string(
            'title', label='Title',
            description='The title for the plot.')
        parameters.set_string(
            'y_label', label='Y Label',
            description='A label for the Y axis.')
        parameters.set_string(
            'bin_labels', label='Bin labels',
            description='A signal with the labels of each bin. '
                        'These are printed along the x axis.',
            editor=synode.editors.combo_editor())
        parameters.set_list(
            'y_signals', label='Y Signals',
            description='Check any signals which should be plotted. '
                        'Each checked signal gets its own color.',
            editor=synode.editors.multilist_editor(mode=False))
        parameters.set_boolean(
            'rotate', label='Rotate bin labels', value=False,
            description='Rotate bin labels to make room for longer labels.')

    def _adjust_parameters(self, parameters, names):
        parameters['bin_labels'].adjust(names.options)
        parameters['y_signals'].adjust(names.options)

    def _get_model(self, parameters, names):
        title = parameters['title'].value
        bin_labels = parameters['bin_labels'].value
        y_sigs = parameters['y_signals'].value_names
        y_label = parameters['y_label'].value
        rotate = parameters['rotate'].value
        plots = [
            {
                "bin_labels": (names.to_expr(bin_labels), "py"),
                "ydata": (names.to_expr(y_sig), "py"),
                "label": (names.to_name(y_sig), "value"),
                "type": "bar"
            }
            for y_sig in y_sigs
        ]
        xaxis = {"position": ("bottom", "value")}
        if rotate:
            xaxis["rot_tick_labels"] = ("Counter clockwise", "value")
        return {
            "axes": [{
                "title": (title, "value"),
                "xaxis": xaxis,
                "yaxis": {
                    "position": ("left", "value"),
                    "label": (y_label, "value")
                },
                "plots": [{
                    "grouping": ("grouped", "value"),
                    "plots": plots,
                    "type": "barcontainer"
                }],
                "legend": {
                    "show": ("True", "value")
                }
            }]}


class PieWizard(Wizard):
    name = 'pie'
    description = "Pie chart."

    def _init_parameters(self, parameters):
        parameters.set_string(
            'title', label='Title',
            description='The title for the plot.')
        parameters.set_string(
            'labels', label='Bin labels',
            description='A signal with the labels of the wedges.',
            editor=synode.editors.combo_editor())
        parameters.set_string(
            'values', label='Values',
            description='A signal with the values of the wedges.',
            editor=synode.editors.combo_editor())
        parameters.set_boolean(
            'percentages', label='Show percentages', value=False,
            description='If checked write the percentage in each wedge.')
        parameters.set_boolean(
            'legend', label='Put labels in legend', value=False,
            description='If checked puts all labels in a legend, '
                        'if unchecked write the labels next to their '
                        'respective pie piece.')

    def _adjust_parameters(self, parameters, names):
        parameters['labels'].adjust(names.options)
        parameters['values'].adjust(names.options)

    def _get_model(self, parameters, names):
        title = parameters['title'].value
        labels = parameters['labels'].value
        values = parameters['values'].value
        legend = parameters['legend'].value
        percentages = parameters['percentages'].value
        axes = {
            "title": (title, "value"),
            "aspect": ("equal", "value"),
            "frameon": ("False", "value"),
            "xaxis": {
                "position": ("bottom", "value"),
                "visible": ("False", "value")
            },
            "yaxis": {
                "position": ("left", "value"),
                "visible": ("False", "value")
            },
            "plots": [{
                "weights": (names.to_expr(values), "py"),
                "labels": (names.to_expr(labels), "py"),
                "type": "pie"
            }]}
        if percentages:
            axes['plots'][0]['autopct'] = ("Auto", "value")
        if legend:
            axes['plots'][0]['labelhide'] = ("True", "value")
            axes['legend'] = {
                "show": ("True", "value"),
                "loc": ("outside right", "value"),
                "distance": ("2.0", "value"),
            }
        return {"axes": [axes]}


class BoxWizard(Wizard):
    name = 'box'
    description = "Creates a box plot of one or more signals."

    def _init_parameters(self, parameters):
        parameters.set_string(
            'title', label='Title',
            description='The title for the plot.')
        parameters.set_string(
            'y_label', label='Y Label',
            description='A label for the Y axis.')
        parameters.set_list(
            'signals', label='Signals',
            description='Check all signals that should be in the plot. Each '
                        'signal gets a box plot showing its distribution.',
            editor=synode.editors.multilist_editor(mode=False))
        parameters.set_boolean(
            'rotate', label='Rotate labels', value=False,
            description='Rotate signal labels to make room for longer labels.')

    def _adjust_parameters(self, parameters, names):
        parameters['signals'].adjust(names.options)

    def _get_model(self, parameters, names):
        title = parameters['title'].value
        signals = parameters['signals'].value_names
        y_label = parameters['y_label'].value
        rotate = parameters['rotate'].value
        ydata = ", ".join(names.to_expr(sig) for sig in signals)
        bin_labels = ", ".join(f"'{names.to_name(sig)}'" for sig in signals)
        xaxis = {"position": ("bottom", "value")}
        if rotate:
            xaxis["rot_tick_labels"] = ("Counter clockwise", "value")
        return {
            "axes": [{
                "title": (title, "value"),
                "xaxis": xaxis,
                "yaxis": {
                    "position": ("left", "value"),
                    "label": (y_label, "value")
                },
                "plots": [{
                    "ydata": (f"[{ydata}]", "py"),
                    "bin_labels": (f"[{bin_labels}]", "py"),
                    "type": "box"
                }]
            }]}


wizard_classes = {
    cls.name: cls for cls in [
        LineWizard,
        BarWizard,
        ScatterWizard,
        BoxWizard,
        PieWizard,
    ]}


class DataModel:
    def __init__(self, data, data_table=None):
        self.instance = uuid.uuid4().bytes
        self._data_table = data_table
        self.set_data(data)

    def set_data(self, data):
        self.model = data
        self.root = models.Root(data)
        self.root.set_data_table(self._data_table)


class ParameterTreeView(qt_model.BaseParameterTreeView):
    def __init__(self, input_table, mime=MIME, parent=None):
        super(ParameterTreeView, self).__init__(input_table, mime, parent)
        self.completer_models = {
            'default':
                (qt_model.SyDataTreeCompleterModel,
                 (self._input_table, ),
                 {'parent': self})
        }

    def add(self, item_cls):
        selected_indices = self.selectedIndexes()
        model = self.model()
        figure_node = self.model().root_item()
        figure_index = model.item_to_index(figure_node)
        if selected_indices:
            selected_index = selected_indices[0]
        else:
            self.setCurrentIndex(figure_index)
            selected_index = figure_index
        selected_item = model.index_to_item(selected_index)

        parent_axes = selected_item.find_first_parent_node_with_class(
            models.Axes)
        if item_cls != models.Axes:
            if not figure_node.has_axes():
                parent_axes = self.add_child(
                    figure_node, models.Axes, figure_index)
            elif parent_axes is None:
                parent_axes = [c for c in figure_node.children if
                               isinstance(c, models.Axes)][0]

        plot_nodes = models.BasePlot, models.BasePlotContainer

        if item_cls in selected_item.valid_children():
            parent_node = selected_item
        elif issubclass(item_cls, models.Axes):
            parent_node = figure_node
        elif issubclass(item_cls, (models.Grid, models.Legend)):
            parent_node = parent_axes
        elif issubclass(item_cls, plot_nodes):
            if isinstance(selected_item, plot_nodes):
                parent_node = selected_item.parent
            else:
                parent_node = parent_axes.plot_container
        elif item_cls not in selected_item.valid_children():
            parent_node = selected_item.parent
        else:
            parent_node = selected_item
        parent_index = model.item_to_index(parent_node)

        if (item_cls in parent_node.valid_children() and
                item_cls in parent_node.get_available_children()):
            new_item = self.add_child(parent_node, item_cls, parent_index)
            new_item_idx = model.item_to_index(new_item)
            self.setCurrentIndex(new_item_idx)

    def drag_move_event_handling(self, event, item_class, index):
        if index.isValid():
            drop_indicator_position = self.dropIndicatorPosition()
            parent_item = index.model().data(index, QtCore.Qt.UserRole)
            if parent_item is None:
                event.ignore()
                return
            if drop_indicator_position != QtWidgets.QAbstractItemView.OnItem:
                # If the drop indicator is not on the item we need to get the
                # parent item in the tree instead.
                parent_item = parent_item.parent
            if item_class in parent_item.get_available_children():
                event.accept()
            else:
                event.ignore()
        else:
            # Only axes items are allowed outside tree (root level).
            # If Plots or PlotContainers are dragged in and no Axes exists, one
            # will be created automatically.
            root = self.model().model.root
            figure = root.find_all_nodes_with_class(models.Figure)[0]
            allowed_super_cls = (models.BasePlot, models.BasePlotContainer)
            if item_class in figure.get_available_children():
                event.accept()
            elif (issubclass(item_class, allowed_super_cls) and
                    not figure.has_axes()):
                # create axes
                axes = models.Axes.create_empty_instance(figure)
                model = self.model()
                figure_index = model.index(0, 0)
                model.insert_node(
                    axes, figure, figure_index, len(figure.children))
                # add item to axes
                event.accept()
            else:
                event.ignore()


class DictStackedWidget(QtWidgets.QStackedWidget):
    """A StackedWidget that stores widgets by key instead of by index."""
    currentChanged = QtCore.Signal(str)
    widgetRemoved = QtCore.Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._indices = []

    def addWidget(self, key, widget):
        """Add a widget with key."""
        super().addWidget(widget)
        self._indices.append(key)

    def insertWidget(self, key, widget):
        """Synonym to addWidget"""
        self.addWidget(key, widget)

    def currentKey(self):
        """Return the current key or None if there are no child widgets."""
        index = self.currentIndex()
        if index == -1:
            return None
        else:
            return self._indices[index]

    def setCurrentKey(self, key):
        """Set current widget to that at key."""
        try:
            index = self._indices.index(key)
        except IndexError:
            return
        super().setCurrentIndex(index)
        self.currentChanged.emit(key)

    def setCurrentWidget(self, widget):
        """Set current widget to widget."""
        index = self.indexOf(widget)
        if index == -1:
            return
        else:
            key = self._indices[index]
            self.setCurrentKey(key)

    def widget(self, key):
        """Get widget at key."""
        try:
            index = self._indices.index(key)
        except IndexError:
            return None
        return super().widget(index)

    def removeWidget(self, widget):
        """
        Remove widget from the stacked widget without destroying it or
        changing its parent.
        """
        index = self.indexOf(widget)
        if index == -1:
            return
        else:
            super().removeWidget(widget)
            key = self._indices.pop(index)
            self.widgetRemoved.emit(key)


class ImageMenuItem(QtWidgets.QWidgetAction):
    """A menu item consisting of a large image."""
    def __init__(self, kind, tooltip, *, parent=None):
        super().__init__(parent)
        self._kind = kind
        self._tooltip = tooltip

    def createWidget(self, parent):
        icon = icon_utils.create_icon(getattr(
            icon_utils.SvgIcon, f"{self._kind}_wizard"))
        button = QtWidgets.QPushButton(parent=parent)
        button.setIcon(icon)
        button.setIconSize(QtCore.QSize(200, 100))
        button.setToolTip(self._tooltip)
        button.clicked.connect(self.triggered)
        return button


class FigureFromTableWidget(ParameterView):
    def __init__(self, input_table, parameters, parent=None):
        super().__init__(parent=parent)

        self.input_table = input_table
        self.parameters = parameters

        self._data_model = DataModel(parameters.value,
                                     data_table=self.input_table)
        self._model = qt_model.TreeItemModel(
            self._data_model, root_cls=models.Figure,
            item_type_to_class=ITEM_TYPE_TO_CLASS, mime=MIME)

        self._wizards = {name: None for name in wizard_classes.keys()}

        self._init_gui()
        self._init_from_parameters()

        exported_config = self._data_model.root.export_config()
        self._curr_config = exported_config

        self._poll_timer = QtCore.QTimer()
        self._poll_timer.setInterval(300)
        self._poll_timer.timeout.connect(self._poll_changes)
        self._poll_timer.start()

    def _init_gui(self):
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)

        self.stacked = DictStackedWidget()

        self.param_tree = ParameterTreeView(
            self.input_table, mime=MIME, parent=self)
        self.param_tree.setModel(self._model)

        self.toolbar = qt_model.BaseItemsToolBar(
            self.param_tree, TOOLBAR_ITEMS, mime=MIME, parent=self)
        self.toolbar.addSeparator()
        wizard_menu_button = QtWidgets.QToolButton(self)
        wizard_menu_button.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        icon = icon_utils.create_icon(icon_utils.SvgIcon.wizard)
        wizard_menu_button.setIcon(icon)
        wizard_menu_button.setToolTip(
            "Simplified guis for specific plot types.")
        self._wizard_menu = QtWidgets.QMenu(self)
        for name, wizard_cls in wizard_classes.items():
            wizard_action = ImageMenuItem(
                name, wizard_cls.description, parent=self)
            wizard_action.triggered.connect(
                functools.partial(self._show_wizard, name))
            self._wizard_menu.addAction(wizard_action)
        wizard_menu_button.setMenu(self._wizard_menu)
        self.toolbar.addWidget(wizard_menu_button)

        tree_layout = QtWidgets.QVBoxLayout()
        tree_layout.setSpacing(0)
        tree_layout.addWidget(self.toolbar)
        tree_layout.addWidget(self.param_tree)

        tree_container = QtWidgets.QWidget()
        tree_container.setLayout(tree_layout)
        self.stacked.addWidget('tree', tree_container)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.stacked)
        self.setLayout(main_layout)

        # Create end wizard action
        self._end_wizard_action = QtWidgets.QAction(self, 'end_wizard')
        icon = icon_utils.create_icon(icon_utils.SvgIcon.back)
        self._end_wizard_action.setIcon(icon)
        self._end_wizard_action.setToolTip(
            "Go back to advanced configuration view, keeping all changes.")
        self._end_wizard_action.triggered.connect(self._hide_wizard)

    def _init_wizard(self, name):
        # class WizardDialog(QtWidgets.QDialog):
        #     def __init__(self, widget):
        #         super().__init__()

        #         buttons = QtWidgets.QDialogButtonBox(
        #             QtWidgets.QDialogButtonBox.Ok
        #             | QtWidgets.QDialogButtonBox.Cancel,
        #             parent=self)
        #         buttons.accepted.connect(self.accept)
        #         buttons.rejected.connect(self.reject)

        #         layout = QtWidgets.QVBoxLayout()
        #         layout.addWidget(widget)
        #         layout.addWidget(buttons)
        #         self.setLayout(layout)

        # self._dialog = WizardDialog(wizard_gui)
        # self._dialog.show()

        wizard_cls = wizard_classes[name]
        wizard = wizard_cls(self._model)

        toolbar = SyBaseToolBar()
        toolbar.addAction(self._end_wizard_action)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(wizard.gui())
        wizard_gui = QtWidgets.QWidget()
        wizard_gui.setLayout(layout)
        self.stacked.addWidget(name, wizard_gui)

        self._wizards[name] = wizard
        wizard.wizard_changed.connect(
            functools.partial(self._wizard_changed, name))

    def _show_wizard(self, name):
        self._wizard_menu.close()
        # res = QtWidgets.QMessageBox.question(
        #     self, "Clear figure?",
        #     "This will clear the current configuration. "
        #     "Are you sure you want to preceed?")
        # if res == QtWidgets.QMessageBox.No:
        #     return

        if self._wizards[name] is None:
            self._init_wizard(name)
        self.stacked.setCurrentKey(name)
        self._wizard_changed(name)

    def _wizard_changed(self, name):
        self._model.set_data(self._wizards[name].get_model())
        self.expand_axes()

    def _hide_wizard(self):
        self.stacked.setCurrentKey('tree')

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.param_tree.resizeColumnToContents(0)

    def _init_from_parameters(self):
        self.param_tree.resizeColumnToContents(0)

        # add one axes if empty model
        if not self._model.root_item().has_axes():
            parent_item = self._model.root_item()
            parent_index = self._model.index(-1, -1)
            item_class = self._model.item_type_to_class['axes']
            if item_class not in parent_item.valid_children():
                return False
            new_item = item_class.create_empty_instance(parent_item)

            self._model.beginInsertRows(parent_index, 0, 0)
            base_models.insert_node(new_item, parent_item, 0)
            self._model.endInsertRows()

        self.expand_axes()

    def expand_axes(self):
        # expand all axes
        num_axes = self._model.rowCount()
        for i in range(num_axes):
            index = self._model.index(i, 0)
            self.param_tree.setExpanded(index, True)
            # expand all Plots
            for row in range(self._model.rowCount(index)):
                child_index = self._model.index(row, 0, index)
                item = self._model.index_to_item(child_index)
                if isinstance(item, models.Plots):
                    self.param_tree.setExpanded(child_index, True)

    def save_parameters(self):
        if self.param_tree.state() == QtWidgets.QAbstractItemView.EditingState:
            index = self.param_tree.currentIndex()
            self.param_tree.currentChanged(index, index)
        self._save_parameters()

    def _save_parameters(self):
        self.parameters.value = self._data_model.root.export_config()

    def cleanup(self):
        self._poll_timer.timeout.disconnect(self._poll_changes)
        self._poll_timer.stop()

    def _poll_changes(self):
        # Resetting internal counter between calls to save parameters.
        self._data_model.root._given_ids.clear()
        exported_config = self._data_model.root.export_config()
        new_config = json.dumps(exported_config)
        if new_config != self._curr_config:
            self._curr_config = new_config
            self._save_parameters()

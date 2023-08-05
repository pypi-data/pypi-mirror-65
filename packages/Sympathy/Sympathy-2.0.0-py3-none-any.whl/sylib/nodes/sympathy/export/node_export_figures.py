# This file is part of Sympathy for Data.
# Copyright (c) 2016, 2017, Combine Control Systems AB
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
from sympathy.api import node as synode
from sympathy.api.nodeconfig import Port, Ports, Tag, Tags, deprecated_node
from sympathy.api import exporters
from sylib.export import base


class ExportFigures(base.ExportMultiple, synode.Node):
    """
    Export Figures to a selected data format.

    :Ref. nodes:
        :ref:`org.sysess.sympathy.visualize.figure`,
        :ref:`org.sysess.sympathy.visualize.figures`
    """

    name = 'Export Figures'
    description = 'Export Figures to image files.'
    icon = 'export_figure.svg'
    tags = Tags(Tag.Output.Export)
    author = 'Benedikt Ziegler'
    nodeid = 'org.sysess.sympathy.export.exportfigures'
    version = '0.2'
    inputs = Ports([Port.Figures('Input figures', name='figures'),
                    Port.Datasources(
                        'External filenames',
                        name='port1', n=(0, 1, 0))])
    plugins = (exporters.FigureDataExporterBase, )
    parameters = base.base_params()

    def update_parameters(self, old_params):
        extension = old_params._parameter_dict.pop('extension', None)
        width = old_params._parameter_dict.pop('width', None)
        height = old_params._parameter_dict.pop('height', None)
        if 'custom_exporter_data' not in old_params:
            custom_exporter_data = old_params.create_group(
                'custom_exporter_data')
        else:
            custom_exporter_data = old_params['custom_exporter_data']
        if 'Image' not in custom_exporter_data:
            image = custom_exporter_data.create_group('Image')
        else:
            image = custom_exporter_data['Image']
        if extension is not None:
            image.set_list('extension',
                           label=extension['label'],
                           description=extension['description'],
                           value=extension['value'],
                           plist=extension['list'],
                           editor=extension['editor'])
        if width is not None:
            image.set_integer('width',
                              label=width['label'],
                              description=width['description'],
                              value=width['value'],
                              editor=width['editor'])
        if height is not None:
            image.set_integer('height',
                              label=height['label'],
                              description=height['description'],
                              value=height['value'],
                              editor=height['editor'])
        return old_params


@deprecated_node('3.0.0', 'Export Figures (with optional datasource port)')
class ExportFiguresWithDsrcs(base.ExportMultiple, synode.Node):
    """
    Export Figures to a selected data format with a list of datasources for
    output paths.
    """

    name = 'Export Figures with Datasources'
    description = 'Export Figures to image files.'
    icon = 'export_figure.svg'
    tags = Tags(Tag.Output.Export)
    author = 'Magnus Sandén'
    nodeid = 'org.sysess.sympathy.export.exportfigureswithdscrs'
    version = '0.1'

    inputs = Ports([
        Port.Figures('Input figures', name='figures'),
        Port.Datasources('Datasources', name='dsrcs')])
    plugins = (exporters.FigureDataExporterBase, )
    parameters = base.base_params()

    def _exporter_ext_filenames_portname(self):
        return 'dsrcs'

    def _exporter_ext_filename(self, custom_parameters, filename):
        if not os.path.splitext(filename)[1]:
            ext = custom_parameters['extension'].selected
            filename = '{}.{}'.format(filename, ext)
        return filename

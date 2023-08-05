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
"""
These two nodes takes the structure of an ADAF or ADAFs (Type, System, Raster,
and Parameter) and outputs it to a Table or Tables.
"""
import numpy as np

from sympathy.api import node as synode
from sympathy.api import node_helper
from sympathy.api.nodeconfig import Port, Ports, Tag, Tags


class ADAFStructureTable(synode.Node):
    """Creates Table from the structure of the ADAF."""

    author = 'Erik der Hagopian'
    version = '1.0'
    icon = 'adaf2adafs.svg'

    name = 'ADAF structure to Table'
    description = 'Creates Table from the structure of the ADAF.'
    nodeid = 'org.sysess.sympathy.data.adaf.adafstructuretable'
    tags = Tags(Tag.DataProcessing.Index)

    inputs = Ports([Port.ADAF('Input ADAF', name='port1')])
    outputs = Ports([Port.Table('ADAF structure as Table', name='port1')])

    @staticmethod
    def run(input_file, output_file):
        def adaf_iterator(adaf_file):
            yield ('Metadata', '', '', adaf_file.meta.keys())
            yield ('Result', '', '', adaf_file.res.keys())
            for system_key, system_value in adaf_file.sys.items():
                for raster_key, raster_value in system_value.items():
                    yield ('Timeseries', system_key, raster_key,
                           raster_value.keys())

        type_column = []
        system_column = []
        raster_column = []
        parameter_column = []
        index_column = []

        output_info = [('Type', type_column),
                       ('System', system_column),
                       ('Raster', raster_column),
                       ('Parameter', parameter_column),
                       ('Index', index_column)]

        for i, (type_key, system_key, raster_key,
                parameter_keys) in enumerate(adaf_iterator(input_file)):

            number_of_keys = len(parameter_keys)
            type_column.extend([type_key] * number_of_keys)
            system_column.extend([system_key] * number_of_keys)
            raster_column.extend([raster_key] * number_of_keys)
            parameter_column.extend(parameter_keys)
            index_column.extend([i] * number_of_keys)

        for name, column in output_info:
            output_file.set_column_from_array(name, np.array(column))

    def execute(self, node_context):
        input_file = node_context.input[0]
        output_file = node_context.output[0]
        self.run(input_file, output_file)


@node_helper.list_node_decorator(['port1'], ['port1'])
class ADAFsStructureTables(ADAFStructureTable):
    name = 'ADAFs structure to Tables'
    nodeid = 'org.sysess.sympathy.data.adaf.adafsstructuretables'

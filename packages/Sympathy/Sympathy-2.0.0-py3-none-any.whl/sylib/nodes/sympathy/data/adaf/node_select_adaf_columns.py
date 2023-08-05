# This file is part of Sympathy for Data.
# Copyright (c) 2015, Combine Control Systems AB
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
If you're only interested in some of the data in an ADAF (maybe for performance
reasons) you can use e.g. :ref:`Select columns in ADAF with structure Table`.

The Table/Tables argument shall have four columns, which must be named Type,
System, Raster, and Parameter. These columns hold the names of the
corresponding fields in the ADAF/ADAFs.
"""
import contextlib
from collections import OrderedDict
from sympathy.api import node, table
from sympathy.api import node_helper, dtypes
from sympathy.api.nodeconfig import Port, Ports, Tag, Tags

from sympathy.api.exceptions import SyDataError, sywarn


def apply_selection(in_adaf, out_adaf, meta, res, ts, compliment):
    out_adaf.set_source_id(in_adaf.source_id())

    for in_data, out_data, group in [(in_adaf.meta, out_adaf.meta, meta),
                                     (in_adaf.res, out_adaf.res, res)]:

        in_keys = in_data.keys()
        if compliment:
            keys = [key for key in in_keys if key not in group]
        else:
            keys = [key for key in in_keys if key in group]

        in_table = in_data.to_table()
        if set(keys) == set(in_keys):
            out_table = in_table
        else:
            out_table = table.File()
            for key in keys:
                out_table.update_column(key, in_table)

        out_data.from_table(out_table)

    systems = {}

    for sysname, in_sys in in_adaf.sys.items():
        if not compliment and sysname not in ts:
            continue
        ts_sys = ts.get(sysname, {})

        for rastername, in_raster in in_sys.items():
            if not compliment and rastername not in ts_sys:
                continue
            ts_names = ts_sys.get(rastername, [])
            in_ts_names = in_raster.keys()

            if compliment:
                keys = [key for key in in_ts_names if key not in ts_names]
            else:
                keys = [key for key in in_ts_names if key in ts_names]

            if keys:
                if sysname in systems:
                    out_sys = systems[sysname]
                else:
                    out_sys = out_adaf.sys.create(sysname)
                    systems[sysname] = out_sys
                if set(keys) == set(in_ts_names):
                    out_sys.copy(rastername, in_sys)
                else:
                    out_raster = out_sys.create(rastername)
                    out_raster.update_basis(in_raster)
                    for key in keys:
                        out_raster.update_signal(key, in_raster)


def build_selection(selection):
    selection_columns = ['Type', 'System', 'Raster', 'Parameter']
    columns = selection.column_names()

    if not all([column_name in columns
                for column_name in selection_columns]):
        raise SyDataError(
            'Selection Table must have the following columns: {}\n'
            'Using ADAF structure to Table ensures it.'.format(
                ', '.join(selection_columns)))

    narrow_selection = table.File()

    for column in selection_columns:
        narrow_selection.update_column(column, selection)

        kind = selection.column_type(column).kind
        if kind != 'U':
            msg = (
                'Selection column "{}" needs to be in text format, it is {}. '
                'While this is true, the selection will be ignored.'
                .format(column, dtypes.typename_from_kind(kind)))
            warn('col_type', msg)
    meta = []
    res = []
    syss = {}

    for typec, systemc, rasterc, parameterc in narrow_selection.to_rows():
        if typec == 'Metadata':
            meta.append(parameterc)
        elif typec == 'Result':
            res.append(parameterc)
        elif typec == 'Timeseries':
            sys = syss.setdefault(systemc, {})
            raster = sys.setdefault(rasterc, [])
            raster.append(parameterc)

    return meta, res, syss


def _set_complement_parameter(parameter_root):
    parameter_root.set_boolean(
        'complement', value=False,
        label='Remove selected columns',
        description=(
            'When enabled, the selected columns will be removed. '
            'When disabled, the non-selected columns will be '
            'removed.'))


_warn_once = False
_warn_categories = set()


@contextlib.contextmanager
def set_warn_once():
    global _warn_once
    global _warn_categories

    _warn_once = True
    _warn_categories = set()
    yield
    _warn_once = False
    _warn_categories = set()


def warn(category, msg):
    global _warn_once
    global _warn_categories

    if not _warn_once:
        sywarn(msg)
    elif category not in _warn_categories:
        sywarn(msg)
        _warn_categories.add(category)


class SelectColumnsADAFWithTable(node.Node):
    name = 'Select columns in ADAF with structure Table'
    author = 'Erik der Hagopian'
    version = '1.0'
    icon = 'select_adaf_columns.svg'
    description = (
        'Select the columns to keep in ADAF using selection table created by '
        'ADAF structure to table')
    nodeid = 'org.sysess.sympathy.data.adaf.selectcolumnsadafwithtable'
    tags = Tags(Tag.DataProcessing.Select)

    inputs = Ports([
        Port.Table('ADAF structure selection', name='selection'),
        Port.ADAF('ADAF data matched with selection', name='data')])
    outputs = Ports([
        Port.ADAF('ADAF data after selection', name='data')])

    parameters = node.parameters()
    _set_complement_parameter(parameters)

    def execute(self, node_context):
        selection = node_context.input['selection']
        in_data = node_context.input['data']
        out_data = node_context.output['data']
        complement = node_context.parameters['complement'].value

        if in_data.is_empty():
            # Result should be empty.
            pass
        elif selection.is_empty():
            if complement:
                out_data.source(in_data)
            else:
                # Result should be empty.
                pass
        else:
            meta, res, syss = build_selection(selection)
            apply_selection(in_data, out_data, meta, res, syss, complement)


@node_helper.list_node_decorator(['data'], ['data'])
class SelectColumnsADAFsWithTable(SelectColumnsADAFWithTable):
    name = 'Select columns in ADAFs with structure Table'
    nodeid = 'org.sysess.sympathy.data.adaf.selectcolumnsadafswithtable'

    def execute(self, node_context):
        with set_warn_once():
            super().execute(node_context)


@node_helper.list_node_decorator(['selection', 'data'], ['data'])
class SelectColumnsADAFsWithTables(SelectColumnsADAFWithTable):
    name = 'Select columns in ADAFs with structure Tables'
    nodeid = 'org.sysess.sympathy.data.adaf.selectcolumnsadafswithtables'

    def execute(self, node_context):
        with set_warn_once():
            super().execute(node_context)

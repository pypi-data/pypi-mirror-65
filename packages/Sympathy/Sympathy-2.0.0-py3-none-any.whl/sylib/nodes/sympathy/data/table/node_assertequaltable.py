# This file is part of Sympathy for Data.
# Copyright (c) 2017, Combine Control Systems AB
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
import numpy as np

from sympathy.api import node
from sympathy.api.nodeconfig import Port, Ports, Tag, Tags
from sympathy.api.exceptions import SyDataError


class AssertEqualTable(node.Node):
    """Compare two incoming tables and raise an error if they differ."""

    name = 'Assert Equal Table'
    author = u'Magnus Sandén'
    version = '1.0'
    icon = ''
    description = ''
    nodeid = 'org.sysess.sympathy.data.table.assertequaltable'
    icon = 'assert_equal.svg'
    tags = Tags(Tag.Development.Test)

    inputs = Ports([
        Port.Table('Table A', name='table1'),
        Port.Custom('table', 'Table B', name='table2', n=(1, None))])
    outputs = Ports([
        Port.Table('Output Table', name='out')])

    parameters = node.parameters()
    parameters.set_boolean(
        'col_order', value=True, label='Compare column order',
        description='Differing column order will trigger error')
    parameters.set_boolean(
        'col_attrs', value=True, label='Compare column attributes',
        description='Differing column attributes will trigger error')
    parameters.set_boolean(
        'tbl_names', value=True, label='Compare table names',
        description='Differing table name will trigger error')
    parameters.set_boolean(
        'tbl_attrs', value=True, label='Compare table attributes',
        description='Differing table attributes will trigger error')
    parameters.set_boolean(
        'inexact_float', value=False, label='Approximate comparison of floats',
        description='If any arithemtics is invovled floats should probably '
                    'be compared approximately.')
    parameters.set_float(
        'rel_tol', value=1e-5, label='Relative tolerance',
        description='Floats are considered unequal if the relative difference '
                    'between them is larger than this value.',
        editor=node.editors.decimal_spinbox_editor(step=1e-5, decimals=10))
    parameters.set_float(
        'abs_tol', value=1e-8, label='Absolute tolerance',
        description='Floats are considered unequal if the absolute difference '
                    'between them is larger than this value.',
        editor=node.editors.decimal_spinbox_editor(step=1e-8, decimals=10))

    controllers = node.controller(
        when=node.field('inexact_float', 'checked'),
        action=(node.field('rel_tol', 'enabled'),
                node.field('abs_tol', 'enabled')))

    def execute(self, node_context):
        parameters = node_context.parameters
        table1 = node_context.input['table1']
        out_table = node_context.output['out']
        inexact_float = parameters['inexact_float'].value
        rel_tol = parameters['rel_tol'].value
        abs_tol = parameters['abs_tol'].value
        col_order = parameters['col_order'].value
        col_attrs = parameters['col_attrs'].value
        tbl_names = parameters['tbl_names'].value
        tbl_attrs = parameters['tbl_attrs'].value

        for table2 in node_context.input.group('table2'):
            self._compare_table(
                table1, table2, col_order, col_attrs, tbl_names,
                tbl_attrs, inexact_float, rel_tol, abs_tol)

        # Could use either one. They are equal after all.
        out_table.source(table1)

    def _compare_table(self, table1, table2, col_order, col_attrs, tbl_names,
                       tbl_attrs, inexact_float, rel_tol, abs_tol):

        # Column names/order
        t1_cols = set(table1.column_names())
        t2_cols = set(table2.column_names())
        if t1_cols != t2_cols:
            only_in_a = t1_cols - t2_cols
            if only_in_a:
                raise SyDataError(
                    "Tables are not equal. Some columns only exist in "
                    "table A: {}".format(list(only_in_a)))
            only_in_b = t2_cols - t1_cols
            if only_in_b:
                raise SyDataError(
                    "Tables are not equal. Some columns only exist in "
                    "table B: {}".format(list(only_in_b)))

            # Should never happen.
            raise SyDataError(
                'Tables are not equal. Different column names.')
        if col_order:
            if table1.column_names() != table2.column_names():
                raise SyDataError(
                    'Tables are not equal. Different column order.')

        # Column data/attributes
        if table1.number_of_rows() != table2.number_of_rows():
            raise SyDataError(
                "Tables are not equal. Different number of rows.")
        for col_name in table1.column_names():
            column1 = table1.get_column_to_array(col_name)
            column2 = table2.get_column_to_array(col_name)

            # Dtypes
            if column1.dtype.kind != column2.dtype.kind:
                raise SyDataError(
                    "Tables are not equal. Different column data type for "
                    "column '{}'.".format(col_name))

            # Masks
            if isinstance(column1, np.ma.MaskedArray):
                mask1 = column1.mask
                column1 = column1.compressed()
            else:
                mask1 = False
            if isinstance(column2, np.ma.MaskedArray):
                mask2 = column2.mask
                column2 = column2.compressed()
            else:
                mask2 = False
            if np.any(mask1 != mask2):
                raise SyDataError(
                    "Tables are not equal. Different masks for column "
                    "'{}'.".format(col_name))

            if inexact_float and column1.dtype.kind == 'f':
                normal_diff = np.logical_not(np.isclose(
                    column1, column2, rel_tol, abs_tol, equal_nan=True))
            else:
                normal_diff = (column1 != column2)

            if column1.dtype.kind == 'f':
                # Need to special case NaN since it isn't equal to itself.
                nans1 = np.isnan(column1)
                nans2 = np.isnan(column2)
                no_nans = np.logical_not(np.logical_or(nans1, nans2))
                normal_diff = np.logical_and(normal_diff, no_nans)
                nan_diff = nans1 != nans2
                diff = np.logical_or(normal_diff, nan_diff)
            else:
                diff = normal_diff

            if diff.any():
                raise SyDataError(
                    "Tables are not equal. "
                    "Different values in column '{}' "
                    "(first difference at row {}).".format(
                        col_name, np.flatnonzero(diff)[0]))
            if col_attrs:
                if (table1.get_column_attributes(col_name) !=
                        table2.get_column_attributes(col_name)):
                    raise SyDataError(
                        "Tables are not equal. Different "
                        "attributes for column '{}'.".format(col_name))

        # Table name/attributes
        if tbl_names:
            if table1.name != table2.name:
                raise SyDataError(
                    'Tables are not equal. Different table names.')
        if tbl_attrs:
            if (dict(table1.get_table_attributes()) !=
                    dict(table2.get_table_attributes())):
                raise SyDataError(
                    'Tables are not equal. Different table attributes.')

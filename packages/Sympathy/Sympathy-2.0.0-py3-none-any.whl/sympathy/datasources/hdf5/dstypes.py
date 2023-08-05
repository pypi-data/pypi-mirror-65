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
"""HDF5 type constructor module."""
from . dslist import Hdf5List as list_type
from . dsdict import Hdf5Dict as dict_type
from . dsrecord import Hdf5Record as record_type
from . dstable import Hdf5Table as table_type
from . dstext import Hdf5Text as text_type
from . dslambda import Hdf5Lambda as lambda_type
from ... types.types import (TypeList,
                             TypeDict,
                             TypeRecord,
                             TypeTuple,
                             TypeTable,
                             TypeText,
                             TypeFunction,
                             TypeAlias)


def factory(content_type):
    """Return datasource constructor according to content_type."""
    # Construct the child element.
    if isinstance(content_type, TypeList):
        return list_type
    elif isinstance(content_type, TypeDict):
        return dict_type
    elif isinstance(content_type, TypeRecord):
        return record_type
    elif isinstance(content_type, TypeTuple):
        return record_type
    elif isinstance(content_type, TypeTable):
        return table_type
    elif isinstance(content_type, TypeText):
        return text_type
    elif isinstance(content_type, TypeFunction):
        return lambda_type
    elif isinstance(content_type, TypeAlias):
        while isinstance(content_type, TypeAlias):
            content_type = content_type.get()
        return factory(content_type)
    else:
        raise Exception('Unknown content type: {}'.format(type(content_type)))


class Hdf5Factory(object):
    """
    Returns HDF5 type constructors.
    Creates typed instances.
    """
    def factory(self, group, content_type, can_write, can_link):
        """Return contained list slice."""
        return factory(content_type)(self.factory,
                                     group=group,
                                     can_write=can_write,
                                     can_link=can_link)

    def list_type(self, datapointer, container_type):
        """Return the HDF5 list type constructor."""
        return list_type(self.factory,
                         datapointer=datapointer)

    def dict_type(self, datapointer, container_type):
        """Return the HDF5 dict type constructor."""
        return dict_type(self.factory,
                         datapointer=datapointer)

    def record_type(self, datapointer, container_type):
        """Return the HDF5 record type constructor."""
        return record_type(self.factory,
                           datapointer=datapointer)

    def table_type(self, datapointer, container_type):
        """Return the HDF5 table type constructor."""
        return table_type(self.factory,
                          datapointer=datapointer)

    def text_type(self, datapointer, container_type):
        """Return the HDF5 text type constructor."""
        return text_type(self.factory,
                         datapointer=datapointer)

    def lambda_type(self, datapointer, container_type):
        """Return the HDF5 lambda type constructor."""
        return lambda_type(self.factory,
                           datapointer=datapointer)


types = Hdf5Factory()

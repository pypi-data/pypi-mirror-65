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
"""Factory module for datasources."""
from . hdf5.dstypes import types as hdf5
from . text.dstypes import types as text
import numpy as tmp


class DatasourceFactory(object):
    """Returns a data source object for the required data source."""
    datasource_from_scheme = {
        'hdf5': hdf5,
        'text': text,
        'tmp': tmp
    }

    def __init__(self, datapointer):
        self._datapointer = datapointer
        self.types = self.datasource_from_scheme[datapointer.scheme]

    def create_list(self, container_type):
        """Return a list datasource."""
        return self.from_constructor(container_type, self.types.list_type)

    def create_dict(self, container_type):
        """Return a dict datasource."""
        return self.from_constructor(container_type, self.types.dict_type)

    def create_record(self, container_type):
        """Return a record datasource."""
        return self.from_constructor(container_type, self.types.record_type)

    def create_tuple(self, container_type):
        """Return a tuple datasource."""
        return self.from_constructor(container_type, self.types.record_type)

    def create_text(self, container_type):
        """Return a text datasource."""
        return self.from_constructor(container_type, self.types.text_type)

    def create_table(self, container_type):
        """Return a table datasource."""
        return self.from_constructor(container_type, self.types.table_type)

    def create_lambda(self, container_type):
        """Return a lambda datasource."""
        return self.from_constructor(container_type, self.types.lambda_type)

    def from_constructor(self, container_type, constructor):
        """Return a datasource determined by category."""
        return constructor(self._datapointer, container_type)

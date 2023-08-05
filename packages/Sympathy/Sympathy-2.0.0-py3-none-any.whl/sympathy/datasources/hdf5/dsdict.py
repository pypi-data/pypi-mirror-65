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
"""HDF5 dict."""
from . import dsgroup


class Hdf5Dict(dsgroup.Hdf5Group):
    """Abstraction of an HDF5-dict."""
    def __init__(self, factory, group=None, datapointer=None, can_write=False,
                 can_link=False):
        super(Hdf5Dict, self).__init__(factory, group, datapointer, can_write,
                                       can_link)

    def read_with_type(self, key, content_type):
        """Reads element at key and returns it as a datasource."""
        key = dsgroup.replace_slash(key)
        group = self.group[key]
        return self.factory(group, content_type, self.can_write,
                            self.can_link)

    def write_with_type(self, key, value, content_type):
        """Write group at key and returns the group as a datasource."""
        key_group = self._group_get_or_create(key)

        return self.factory(
            key_group, content_type, self.can_write, self.can_link)

    def link_with(self, key, value):
        key = dsgroup.replace_slash(key)

        if key in self.group:
            assert(False)
        else:
            self.group[key] = value.link()

    def items(self, content_type):
        return [
            (dsgroup.restore_slash(key),
             self.factory(value, content_type, self.can_write, self.can_link))
            for key, value in self.group.items()]

    def contains(self, key):
        return dsgroup.replace_slash(key) in self.group

    def keys(self):
        """Return the keys."""
        return [dsgroup.restore_slash(key) for key in self.group.keys()]

    def size(self):
        """Return the dict size."""
        return len(self.group)

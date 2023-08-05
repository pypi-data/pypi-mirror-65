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
"""Text record."""
from . import dsgroup


class TextRecord(dsgroup.TextGroup):
    """Abstraction of an Text-list."""
    def __init__(self,
                 factory,
                 create_content,
                 datapointer,
                 group=None,
                 can_write=False,
                 container_type=None,
                 create_path=None):
        super(TextRecord, self).__init__(
            factory, create_content, datapointer, group, can_write,
            container_type, create_path)

    def read_with_type(self, key, content_type):
        """Reads element at key and returns it as a datasource."""
        return self.factory(
            self.datapointer, self.group[key], content_type, self.can_write)

    def write_with_type(self, key, value, content_type):
        """Write group at key and returns the group as a datasource."""
        if key in self.group:
            key_group = self.group[key]
        else:
            key_group = self.create_content(content_type)
            self.group[key] = key_group

        return self.factory(
            self.datapointer, key_group, content_type, self.can_write)

    def keys(self):
        """Return the record keys"""
        return self.group.keys()

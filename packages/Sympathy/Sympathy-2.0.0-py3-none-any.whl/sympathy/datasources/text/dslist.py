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
"""Text list."""
from . import dsgroup


class TextList(dsgroup.TextGroup):
    """Abstraction of an Text-list."""
    def __init__(self,
                 factory,
                 create_content,
                 datapointer,
                 group=None,
                 can_write=False,
                 container_type=None,
                 create_path=None):
        super(TextList, self).__init__(
            factory, create_content, datapointer, group, can_write,
            container_type, create_path)

    def read_with_type(self, index, content_type):
        """Reads element at index and returns it as a datasource."""
        return self.factory(
            self.datapointer, self.group[index], content_type, self.can_write)

    def write_with_type(self, index, value, content_type):
        """Write group at index and returns the group as a datasource."""
        key = str(index)

        if key in self.group:
            key_group = self.group[key]
        else:
            key_group = self.create_content(content_type)
            self.group.append(key_group)

        return self.factory(
            self.datapointer, key_group, content_type, self.can_write)

    def size(self):
        """Return the list size."""
        return len(self.group)

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
"""Interfacing with the path string."""
from . types import from_string_expand


BOOL = {'True': True, 'False': False}


class Util(object):
    """
    Util is a convenience class for safely accessing information from a
    datapointer.
    """

    def __init__(self, datapointer):
        self.datapointer = datapointer

    def file_path(self):
        """Return the pointer url path element."""
        return self.datapointer.path

    def path(self):
        """Return the pointer path fragment."""
        return self.datapointer.fragment("path")

    def mode(self):
        """Return the pointer mode fragment, or r if it does not exist."""
        try:
            mode = self.datapointer.fragment("mode")
            assert(mode in ['r', 'r+', 'w'])
        except KeyError:
            mode = 'r'
        return mode

    def datatype(self):
        """Return the pointer data type fragment."""
        dtype = str(from_string_expand(self.datapointer.fragment("type")))
        dtype = dtype.replace('sytable', 'table')
        dtype = dtype.replace('sytext', 'text')
        return dtype

    def type(self):
        return str(from_string_expand(self.datapointer.fragment("type")))

    def abstype(self):
        return str(self.datapointer.fragment("type"))

    def can_write(self):
        """Returns True if the data source can be written, False otherwise."""
        try:
            return self.mode() == 'w'
        except KeyError:
            return False

    def can_link(self):
        """Returns True if the data source can use links, False otherwise.."""
        try:
            return BOOL[self.datapointer.fragment("link")]
        except KeyError:
            return False


class DataPointer(object):
    """Pointer to data."""
    def __init__(self, url):
        self.url = url
        self.scheme, fullpath = url.split('://')

        fragment_id = None
        if '#' in fullpath:
            self.path, fragment_id = fullpath.rsplit('#', 1)
        try:
            fragment_list = fragment_id.split('&')
            self._fragment_dict = dict([tuple(fragment.split('='))
                                        for fragment in fragment_list])
        except AttributeError:
            self._fragment_dict = {}

    def fragment(self, name):
        """Getter for fragment."""
        return self._fragment_dict[name]

    def set_fragment(self, name, value):
        """Setter for fragment."""
        self._fragment_dict[name] = value

    def del_fragment(self, name):
        """Deleter for fragment."""
        del self._fragment_dict[name]

    def util(self):
        """Returns a Util class instance."""
        return Util(self)

    def copy(self):
        """Copy datapointer."""
        return DataPointer(self.url)

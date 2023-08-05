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
from .. utils import complete
from . import sybase
from . import sylist
from . import exception as exc


def _int_index_guard(index):
    if not isinstance(index, int):
        raise TypeError(
            u'Only basic integer indexing is supported, not: "{}"'
            .format(index))


class sytuple(sybase.sygroup):
    def __init__(self, container_type, datasource=sybase.NULL_SOURCE):
        super(sytuple, self).__init__(container_type,
                                      datasource or sybase.NULL_SOURCE)
        self.content_types = []
        self._content_types = []

        for content_type in container_type:
            self.content_types.append(content_type)
            try:
                while True:
                    content_type = content_type.get()
            except AttributeError:
                self._content_types.append(content_type)

        self._cache = [None] * len(container_type)

    def __repr__(self):
        return str(self._cache)

    def __len__(self):
        return len(self._cache)

    def __iter__(self):
        for i in range(len(self._cache)):
            yield self.__getitem__(i)

    def __getitem__(self, index):
        _int_index_guard(index)

        value = self._cache[index]
        if value is None:
            content_type = self.content_types[index]
            try:
                # Read from datasource.
                source = self._datasource.read_with_type(
                    str(index), self._content_types[index])
            except KeyError:
                # Create content without datasource.
                value = self._factory.from_type(content_type)
            else:
                # Create content from datasource.
                source = source or sybase.NullSource
                value = self._factory.from_datasource(
                    source,
                    content_type)
            self._cache[index] = value
        return value

    def __setitem__(self, index, value):
        _int_index_guard(index)
        content_type = self.content_types[index]
        sybase.assert_type(
            self, value.container_type, content_type)
        self._cache[index] = value

    def __copy__(self):
        obj = super(sytuple, self).__copy__()
        obj.content_types = self.content_types
        obj._content_types = self._content_types
        obj._datasource = self._datasource
        obj._cache = list(self._cache)
        return obj

    def __deepcopy__(self, memo=None):
        obj = self.__copy__()
        obj._cache = [None if v is None else v.__deepcopy__()
                      for v in self._cache]
        return obj

    def names(self, kind=None, fields=None, **kwargs):
        return sylist.list_names(self, kind=kind, fields=fields, **kwargs)

    def completions(self, **kwargs):
        def items(ctx):
            return list(range(len(self)))

        builder = complete.builder()
        child_builders = []

        for k in range(len(self)):
            child = self[k]
            child_builder = child.completions()
            child_builders.append(child_builder)

        builder.getitem(items, child_builders)
        return builder

    def update(self, other):
        sybase.assert_type(
            self, self.container_type, other.container_type)
        self._cache = list(other)

    def source(self, other, shallow=False):
        if shallow:
            self.update(other)
        else:
            self.update(other.__deepcopy__())

    def writeback(self):
        super(sytuple, self).writeback()

    def _writeback(self, datasource, link=None):
        origin = self._datasource
        target = datasource
        exc.assert_exc(target.can_write, exc=exc.WritebackReadOnlyError)
        shared_origin = target.shares_origin(origin)
        linkable = not shared_origin and target.transferable(origin)

        if link:
            return False

        for i, value in enumerate(self._cache):
            key = str(i)
            if value is None:
                if linkable and target.write_link(key, origin, key):
                    pass
                else:
                    value = self[i]

            if value is not None and not value._writeback(target, key):
                new_target = target.write_with_type(
                    key, value, self._content_types[i])
                value._writeback(new_target)
        return True

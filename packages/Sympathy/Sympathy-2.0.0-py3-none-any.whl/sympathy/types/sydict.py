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
"""Sympathy dict type."""
from .. utils import complete
from .. utils import names as names_m
from . import sybase
from . import exception as exc


class sydict(sybase.sygroup):
    """A type representing a dict."""
    def __init__(self, container_type, datasource=sybase.NULL_SOURCE,
                 items=None):
        """Init."""
        super(sydict, self).__init__(container_type,
                                     datasource or sybase.NULL_SOURCE)

        self.content_type = self.container_type.element()
        self._content_type = self.content_type

        try:
            while True:
                self._content_type = self._content_type.get()
        except AttributeError:
            pass

        if datasource is sybase.NULL_SOURCE:
            self._cache = {} if items is None else dict(items)
        else:
            self._cache = dict.fromkeys(datasource.keys())

        self.__all_cached = False

    def keys(self):
        """Returns all contained keys."""
        return self._cache.keys()

    def items(self):
        """Returns all contained items as a tuple list."""
        self.__cache_all()
        return self._cache.items()

    def values(self):
        """Returns all contained values as a list."""
        self.__cache_all()
        return self._cache.values()

    def iterkeys(self):
        """Returns iterator for all contained keys."""
        return iter(self._cache.keys())

    def iteritems(self):
        """Returns iterator for all contained items."""
        for key, value in self._cache.items():
            if value is None:
                yield (key, self[key])
            else:
                yield (key, value)
        self.__all_cached = True

    def itervalues(self):
        """Returns iterator for all contained values."""
        return (value for key, value in self.iteritems())

    def update(self, other):
        """Update dict with other dict."""
        if isinstance(other, sydict):
            sybase.assert_type(self, other.container_type,
                               self.container_type)
            self._cache.update(dict(other.items()))
        else:
            try:
                items = other.items()
            except AttributeError:
                items = other

            for _, v in items:
                sybase.assert_type(self, v.container_type,
                                   self.content_type)
            self._cache.update(items)

    def source(self, other, shallow=False):
        if shallow:
            self.update(other)
        else:
            self.update(other.__deepcopy__())

    def __copy__(self):
        obj = super(sydict, self).__copy__()
        obj.content_type = self.content_type
        obj._content_type = self._content_type
        obj.__all_cached = self.__all_cached
        obj._cache = dict(self._cache)
        return obj

    def __deepcopy__(self, memo=None):
        obj = self.__copy__()
        obj._cache = {k: None if v is None else v.__deepcopy__()
                      for k, v in iter(self._cache.items())}
        return obj

    def names(self, kind=None, fields=None, **kwargs):
        def calc_quote(text):
            return repr(text)

        names = names_m.names(kind, fields, store_created=False)
        kind, fields = names.updated_args()
        fields_list = names.fields()

        for key, value in self.iteritems():
            for n in value.names(kind=kind, fields=fields_list):
                item = names.create_item(n)
                for f in fields_list:
                    if f == 'expr':
                        item[f] = '[{}]{}'.format(
                            calc_quote(key), n.get(f, ''))
                    elif f == 'path':
                        v = [('[]', key)]
                        v.extend(n.get(f, default=[]))
                        item[f] = v
                yield names.item_to_result(item)

    def completions(self):
        def calc_quote(text):
            return repr(text)

        def items(ctx):
            return self.keys()

        builder = complete.builder()
        return builder.getitem(items)

    def visit(self, group_visitor):
        """Accept group visitior."""
        group_visitor.visit_dict(self)

    def __contains__(self, key):
        """Check if string key is one of the sydict keys."""
        return key in self._cache

    def __len__(self):
        return len(self._cache)

    def __repr__(self):
        self.__cache_all()
        return str(self._cache)

    def __delitem__(self, key):
        del self._cache[key]

    def __iter__(self):
        return self.iterkeys()

    def __getitem__(self, key):
        """Get item."""
        value = self._cache[key]
        if value is None:
            value = self._factory.from_datasource(
                self._datasource.read_with_type(key, self.content_type),
                self.content_type)
            self._cache[key] = value
        return value

    def __setitem__(self, key, item):
        """Set item."""
        sybase.assert_type(self, item.container_type,
                           self.content_type)
        self._cache[key] = item

    def __cache_all(self):
        """Internal method for caching all values from the datasource."""
        if self.__all_cached:
            return
        for key, value in self._cache.items():
            self._cache[key] = self[key]
        self.__all_cached = True

    def writeback(self):
        super(sydict, self).writeback()

    def _writeback(self, datasource, link=None):
        origin = self._datasource
        target = datasource
        exc.assert_exc(target.can_write, exc=exc.WritebackReadOnlyError)
        shared_origin = target.shares_origin(origin)
        linkable = not shared_origin and target.transferable(origin)

        if link:
            return False

        for key, value in iter(self._cache.items()):
            if value is None:
                if linkable and target.write_link(key, origin, key):
                    pass
                else:
                    value = self[key]

            if value is not None:
                if not value._writeback(target, key):
                    new_target = target.write_with_type(
                        key, value, self._content_type)
                    value._writeback(new_target)

        return True

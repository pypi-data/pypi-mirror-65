# This file is part of Sympathy for Data.
# Copyright (c) 2016, Combine Control Systems AB
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

import collections


def _func(f):
    return f.__func__


def _self(f):
    return f.__self__


def _class(f):
    return f.__class__


class Event(object):
    """
    Basic event framework for in thread callbacks.
    """

    def __init__(self, *args, **kwargs):
        self._handlers = collections.OrderedDict()

    def add_handler(self, method):
        self._handlers[(_self(method), _func(method))] = None

    def remove_handler(self, method):
        self._handlers.pop((_self(method), _func(method)), None)

    def emit(self, *args, **kwargs):
        for obj, func in self._handlers:
            func(obj, *args, **kwargs)

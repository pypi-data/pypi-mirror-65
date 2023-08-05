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
"""Factory module for sympathy level types."""
from hashlib import sha1
import logging

from . datapointer import DataPointer
from . types import (
    TypeRecord, TypeList, TypeDict, TypeTable, TypeText, TypeAlias,
    TypeFunction, TypeTuple, TypeGeneric, parse_base_line)
from . types import manager as type_manager
from . import sybase
from . sydict import sydict
from . import sylist
from . syrecord import syrecord
from . sytable import sytable
from . sytext import sytext
from . sygeneric import sygeneric
from . sylambda import sylambda
from . sytuple import sytuple
from .. datasources.factory import DatasourceFactory


SyList = sylist.sylist
core_logger = logging.getLogger('core')


class SyFactory(object):
    """Factory for sybase types."""

    def __init__(self, sygroup, creator):
        self.sygroup = sygroup
        self.creator = creator

    def from_datapointer(self, datapointer, container_type, managed=False):
        """Create and return sygroup matching parameters."""
        # Create a relevant data source.
        sydata = None

        if not self.creator:
            return self.sygroup(None)
        else:
            datasource = self.creator(
                DatasourceFactory(datapointer))(container_type)

            try:
                sydata = self.sygroup(container_type, datasource, managed)
            except TypeError:
                sydata = self.sygroup(container_type, datasource)

            if managed and isinstance(container_type, TypeList):
                if sydata.can_write():
                    sylist.set_write_through(sydata)
                else:
                    sylist.set_read_through(sydata)

            return sydata

    def from_datasource(self, datasource, container_type):
        """Create and return sygroup matching parameters."""
        container_type = type_manager.normalize_instance(container_type)
        return self.sygroup(container_type, datasource)

    def from_type(self, container_type):
        """Create and return sygroup matching parameters."""
        container_type = type_manager.normalize_instance(container_type)
        return self.sygroup(container_type)


SYTYPE_FACTORIES = {
    TypeDict: sydict,
    TypeList: SyList,
    TypeRecord: syrecord,
    TypeTuple: sytuple,
    TypeText: sytext,
    TypeTable: sytable,
    TypeFunction: sylambda,
    TypeGeneric: sygeneric,
}


DSTYPE_FACTORIES = {
    TypeDict: lambda factory: factory.create_dict,
    TypeList: lambda factory: factory.create_list,
    TypeRecord: lambda factory: factory.create_record,
    TypeTuple: lambda factory: factory.create_tuple,
    TypeText: lambda factory: factory.create_text,
    TypeTable: lambda factory: factory.create_table,
    TypeFunction: lambda factory: factory.create_lambda,
    TypeGeneric: None
}


def typealias(container_type, datasource=sybase.NULL_SOURCE, managed=False):
    aliases = []

    while isinstance(container_type, TypeAlias):
        aliases.append(container_type)
        container_type = container_type.get()

    syresult = SYTYPE_FACTORIES[
        type(container_type)](container_type, datasource)

    result = syresult
    raliases = reversed(aliases)

    for alias in raliases:
        util = type_manager.get_typealias_util(alias.name())
        result = util(fileobj=result, managed=managed)

    return result


def create_typealias(factory, container_type):
    while isinstance(container_type, TypeAlias):
        container_type = container_type.get()
    return _ds_factory(container_type)(factory)(container_type)


FACTORIES = {
    TypeDict: SyFactory(sydict, lambda factory: factory.create_dict),
    TypeList: SyFactory(SyList, lambda factory: factory.create_list),
    TypeRecord: SyFactory(syrecord, lambda factory: factory.create_record),
    TypeTuple: SyFactory(sytuple, lambda factory: factory.create_tuple),
    TypeText: SyFactory(sytext, lambda factory: factory.create_text),
    TypeTable: SyFactory(sytable, lambda factory: factory.create_table),
    TypeFunction: SyFactory(sylambda, lambda factory: factory.create_lambda),
    TypeAlias: SyFactory(
        typealias, lambda factory: lambda container_type:
        create_typealias(factory, container_type)),
    TypeGeneric: SyFactory(sygeneric, None)
}


class UnsupportedType(Exception):
    pass


def _factory(factory_mapping, container_type):
    try:
        return factory_mapping[type(container_type)]
    except KeyError:
        raise UnsupportedType(
            '{}: "{}"'.format(type(container_type), container_type))


def _sy_factory(container_type):
    return _factory(FACTORIES, container_type)


def _ds_factory(container_type):
    return _factory(DSTYPE_FACTORIES, container_type)


class TypeFactory(object):
    """ Factory for types """

    def __init__(self):
        """Init"""
        self.types = {}

    def from_url(self, url, managed=False):
        """Create and return sympathy level type matching url."""
        data_pointer = DataPointer(url)
        typestring = data_pointer.fragment('type')
        container_type = None

        if type_manager.has_typealias_definition(typestring):
            container_type = type_manager.get_typealias_definition(
                typestring)
        else:
            hash_name = sha1(typestring.encode('ascii')).hexdigest()
            legal_name = 'k' + hash_name
            try:
                container_type = self.types[legal_name]
            except KeyError:
                container_type = parse_base_line(typestring)

        try:
            type_manager.normalize()
        except KeyError:
            core_logger.warn('Fixme! Bad typealias in type manager.')
        return _sy_factory(container_type).from_datapointer(
            data_pointer, container_type, managed)

    def from_datasource(self, datasource, container_type):
        """
        Create and return sympathy level type matching datasource and
        container type.
        """
        container_type = type_manager.normalize_instance(container_type)
        return _sy_factory(container_type).from_datasource(
            datasource, container_type)

    def from_type(self, container_type):
        """Create and return sympathy level type matching container type."""
        container_type = type_manager.normalize_instance(container_type)
        return _sy_factory(container_type).from_type(container_type)


typefactory = TypeFactory()

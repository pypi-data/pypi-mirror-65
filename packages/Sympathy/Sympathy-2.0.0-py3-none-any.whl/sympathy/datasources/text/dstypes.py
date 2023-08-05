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
"""Text type constructor module."""
from . dslist import TextList as list_type
from . dsdict import TextDict as dict_type
from . dsrecord import TextRecord as record_type
from . dstable import TextTable as table_type
from . dstext import TextText as text_type
from . dslambda import TextLambda as lambda_type
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


def create_content(content_type):
    """Return the text group element for the given content type."""
    if isinstance(content_type, TypeList):
        return []
    else:
        return {}


def create_path(container, container_type, path):
    """Create path in file returning the group at container[path]."""

    def create_key(container_type, key):
        """
        Parse string key depending on type.
        Return parsed key.
        """
        if isinstance(container_type, TypeList):
            return int(key)
        else:
            return key

    def set_content(container, container_type, key, value):
        """Set content."""
        if isinstance(container_type, TypeList):
            assert int(key) == container(len)
            container.append(value)
        else:
            container[key] = value

    def update_content(container, container_type, key):
        """
        Get value in container matching key.
        If it does not exist create new value according to type.
        Return tuple of value and its content type.
        """
        key = create_key(container_type, key)
        content_type = container_type[key]

        try:
            content = container[key]
        except KeyError:
            content = create_content(content_type)
            set_content(container, container_type, key, content)
        return (content, content_type)

    root = container

    # Adding other keys.
    for key in [key for key in path.split("/") if key != '']:
        root, container_type = update_content(root, container_type, key)
    return root


class TextFactory(object):
    """
    Returns Text type constructors.
    Creates typed instances.
    """
    def factory(self, datapointer, group, content_type, can_write):
        """Return contained list slice."""
        return factory(content_type)(self.factory,
                                     create_content,
                                     datapointer,
                                     group=group,
                                     can_write=can_write)

    def list_type(self, datapointer, container_type):
        """Return the Text list type constructor."""
        return list_type(self.factory,
                         create_content,
                         datapointer,
                         container_type=container_type,
                         create_path=create_path)

    def dict_type(self, datapointer, container_type):
        """Return the Text dict type constructor."""
        return dict_type(self.factory,
                         create_content,
                         datapointer,
                         container_type=container_type,
                         create_path=create_path)

    def record_type(self, datapointer, container_type):
        """Return the Text record type constructor."""
        return record_type(self.factory,
                           create_content,
                           datapointer,
                           container_type=container_type,
                           create_path=create_path)

    def table_type(self, datapointer, container_type):
        """Return the Text table type constructor."""
        return table_type(self.factory,
                          create_content,
                          datapointer,
                          container_type=container_type,
                          create_path=create_path)

    def text_type(self, datapointer, container_type):
        """Return the Text text type constructor."""
        return text_type(self.factory,
                         create_content,
                         datapointer,
                         container_type=container_type,
                         create_path=create_path)

    def lambda_type(self, datapointer, container_type):
        """Return the Text lambda type constructor."""
        return lambda_type(self.factory,
                           create_content,
                           datapointer,
                           container_type=container_type,
                           create_path=create_path)


types = TextFactory()

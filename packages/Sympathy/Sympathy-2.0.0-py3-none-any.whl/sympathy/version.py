# This file is part of Sympathy for Data.
# Copyright (c) 2017 Combine Control Systems AB
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
major = 2
minor = 0
micro = 0
status = ''
version_tuple = (major, minor, micro, status)

# Intended to be substituted to identify different local versions.
_build_local_version = ""

if _build_local_version:
    version = '{}.{}.{}{}+{}'.format(*version_tuple, _build_local_version)
else:
    version = '{}.{}.{}{}'.format(*version_tuple)


__version__ = version

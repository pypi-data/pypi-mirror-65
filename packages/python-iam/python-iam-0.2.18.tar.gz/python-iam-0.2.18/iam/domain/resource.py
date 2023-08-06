#
# Copyright (C) 2019-2020 Cochise Ruhulessin
#
# This file is part of python-iam.
#
# python-iam is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# python-iam is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with python-iam.  If not, see <https://www.gnu.org/licenses/>.
import uuid

from .resourcekind import ResourceKind
from .resourceuuid import ResourceUUID


class Resource:
    """A value-object representing a resource of a
    specific type.
    """

    @property
    def resource_class(self):
        return type(self).__name__

    @property
    def resource_id(self):
        return self.__resource_id

    @property
    def kind(self):
        return f'{self.api_version}/{self.resource_class}'

    @classmethod
    def fromdjango(cls, obj):
        """Create a :class:`Resource` instance from
        a Django model class or instance.
        """
        return cls(
            ResourceKind.fromdjango(obj),
            ResourceUUID.fromdjango(obj)
        )

    def __init__(self, resource_class, resource_id):
        self.__resource_class = resource_class
        self.__resource_id = resource_id

    def iscomposite(self):
        """Return a boolean indicating if the resource
        identity is a composity.
        """
        return False

    def __repr__(self):
        return f"<iam.{self.__class__.__name__}: {self.resource_id}>"

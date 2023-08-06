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


class ResourceUUID(uuid.UUID):

    @classmethod
    def fromdjango(cls, obj):
        """Create a :class:`ResourceUUID` object from
        a Django model class or instance.
        """
        pk = obj.pk
        meta = obj._meta
        if not isinstance(pk, (int, uuid.UUID))\
        and not hasattr(obj, 'get_resource_id'):
            raise ValueError(
                "Cannot determine resource identifier from primary key.")
        if hasattr(obj, 'get_resource_id'):
            resource_id = obj.get_resource_id()
        elif isinstance(pk, int):
            resource_id = uuid.UUID(int=pk)
        elif isinstance(pk, uuid.UUID):
            resource_id = pk
        return cls(resource_id.hex)

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

from .principal import Principal


class PrincipalFactory:
    """Creates :class:`~iam.domain.principal.Principal`
    instances from Django objects.
    """
    model = Principal

    def fromdjangomodel(self, resource):
        pk = resource.pk
        meta = resource._meta
        if not hasattr(resource, 'kind'):
            raise TypeError("Principal must expose a `kind` attribute.")
        if not isinstance(pk, (int, uuid.UUID))\
        and not hasattr(resource, 'get_resource_id'):
            raise ValueError(
                "Cannot determine resource identifier from primary key.")
        if hasattr(resource, 'get_resource_id'):
            resource_id = resource.get_resource_id()
        elif isinstance(pk, int):
            resource_id = uuid.UUID(int=pk)
        elif isinstance(pk, uuid.UUID):
            resource_id = pk
        return self.model(resource.kind, resource_id)

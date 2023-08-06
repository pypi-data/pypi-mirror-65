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
"""Declares :class:`Principal`."""
import re

from .resource import Resource


class Principal(Resource):
    """Identifies a Subject."""
    api_version = 'iam.unimatrixone.io/v1'
    pattern = '^$'

    @classmethod
    def iscapable(cls, value):
        """Return if the value is correct for the principal type."""
        return bool(re.match(cls.pattern, value))

    def __init__(self):
        self.subject = None

    def isresolved(self):
        """Return a boolean indicating if the :term:`Principal` is resolved
        to a :term:`Subject`.
        """
        return self.subject is not None

    def resolve(self, realm, resolver):
        """Resolves the :term:`Principal` to a :term:`Subject` using
        the given resolver.
        """
        self.subject = resolver.resolve(realm, self)
        return self.subject

    def __repr__(self):
        return f"<iam.{self.__class__.__name__}: {self.value}>"

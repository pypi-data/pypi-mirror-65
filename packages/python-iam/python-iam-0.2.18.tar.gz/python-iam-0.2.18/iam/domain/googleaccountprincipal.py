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
"""Declares :class:`~GoogleAccountPrincipal`."""
from .externalidentifierprincipal import ExternalIdentifierPrincipal


class GoogleAccountPrincipal(ExternalIdentifierPrincipal):
    """A :term:`Principal` that identifies a :term:`Subject` using a
    Google Account ID.
    """
    resource_class = 'GoogleAccountPrincipal'
    platform = 'google'

    @classmethod
    def fromoauth2(cls, response):
        """Instantiate a new :class:`GoogleAccountPrincipal` from the OAuth2
        response received by Google.

        Args:
            response (:obj:`dict`): a dictionary holding the response data.

        Returns:
            :class:`GoogleAccountPrincipal`
        """
        return cls(response['sub'])

    def __init__(self, sub):
        super().__init__()
        self.sub = sub

    @property
    def value(self):
        return self.sub

    def __str__(self):
        return self.sub


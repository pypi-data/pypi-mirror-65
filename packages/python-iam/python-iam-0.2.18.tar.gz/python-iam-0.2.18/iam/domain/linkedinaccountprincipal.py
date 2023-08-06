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
"""Declares :class:`~LinkedInAccountPrincipal`."""
from .externalidentifierprincipal import ExternalIdentifierPrincipal


class LinkedInAccountPrincipal(ExternalIdentifierPrincipal):
    """A :term:`Principal` that identifies a :term:`Subject` using a
    LinkedIn Account ID.
    """
    resource_class = 'LinkedInAccountPrincipal'
    platform = 'linkedin'

    @classmethod
    def fromoauth2(cls, response):
        """Instantiate a new :class:`LinkedInAccountPrincipal` from the OAuth2
        response received by LinkedIn.

        Args:
            response (:obj:`dict`): a dictionary holding the response data.

        Returns:
            :class:`LinkedInAccountPrincipal`
        """
        return cls(response['id'])

    def __init__(self, user_id):
        super().__init__()
        self._id = user_id

    @property
    def value(self):
        return self._id

    def __str__(self):
        return self._id





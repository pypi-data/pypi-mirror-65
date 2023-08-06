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
"""Declares :class:`~EmailPrincipal`."""
import ioc

from .principal import Principal


class EmailPrincipal(Principal):
    """A :term:`Principal` that identifies a :term:`Subject` using an
    email address.
    """
    resource_class = 'EmailPrincipal'
    pattern = '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'

    @property
    def value(self):
        return self.email

    def __init__(self, email):
        super().__init__()
        self.email = str.lower(email)

    @ioc.inject('service', 'EmailService')
    def send(self, service, subject, text, html=None, sender=None):
        return service.send(sender, subject, [self.email], text, html)

    def __str__(self):
        return self.email or ''

"""Declares :class:`PasswordCredential`."""
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password

from .credential import Credential


class PasswordCredential(Credential):

    @property
    def secret(self):
        """Return the secret associated to this :term:`Credential`."""
        return make_password(self.raw_password)

    def __init__(self, raw_password):
        self.raw_password = raw_password
        self.new_password = None

    def cooldown(self):
        """Invoked when the :term:`Principal` with which an authentication
        attempt is being made does not resolve to a user. This is to prevent
        against timing attacks et. al.
        """
        make_password(self.raw_password)

    def check(self, password):
        """Verifies that :attr:`raw_password` matches `password`."""
        if password is None:
            return None

        return check_password(self.raw_password, password,
            lambda x: setattr(self, 'new_password', make_password(x)))

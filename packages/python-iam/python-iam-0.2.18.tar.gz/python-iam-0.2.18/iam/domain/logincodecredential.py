"""Declares :class:`LoginCodeCredential`."""
from .credential import Credential


class LoginCodeCredential(Credential):

    @property
    def secret(self):
        return self.code

    def __init__(self, code):
        self.code = code

"""Declares :class:`GoogleOAuth2`."""
import social_core.backends.google

from .jwe import JWEStateMixin


class GoogleOAuth2(JWEStateMixin, social_core.backends.google.GoogleOAuth2):
    pass

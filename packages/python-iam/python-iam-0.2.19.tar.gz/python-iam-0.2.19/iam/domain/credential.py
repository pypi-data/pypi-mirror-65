"""Declares :class:`Credential`."""
from .resource import Resource


class Credential(Resource):
    """The base class for all :term:`Credentials`."""
    api_version = 'iam.unimatrixone.io/v1'

    def cooldown(self):
        """Invoked when the :term:`Principal` with which an authentication
        attempt is being made does not resolve to a user. This is to prevent
        against timing attacks et. al.
        """
        return

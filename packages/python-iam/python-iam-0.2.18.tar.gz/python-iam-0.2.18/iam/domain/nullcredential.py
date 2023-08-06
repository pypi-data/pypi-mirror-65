"""Declares :class:`NullCredential`."""
from .credential import Credential


class NullCredential(Credential):
    """A :class:`~iam.domain.Credential` implementation that never
    verifies.
    """

    def __init__(self, *args, **kwargs):
        pass

    def check(self, *args, **kwargs):
        """Verifies the credential. Always returns ``False``."""
        return False

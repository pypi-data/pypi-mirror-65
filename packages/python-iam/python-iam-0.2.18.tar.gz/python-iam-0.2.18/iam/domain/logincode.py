"""Declares :class:`LoginCode`."""
import secrets


class LoginCode:
    """Represents a code that a :term:`Subject` may use to authenticate itself
    in a temporary fashion.
    """

    @classmethod
    def new(cls):
        """Return a new :class:`LoginCode` with a random value."""
        return cls(str(secrets.randbelow(999999)).zfill(6))

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

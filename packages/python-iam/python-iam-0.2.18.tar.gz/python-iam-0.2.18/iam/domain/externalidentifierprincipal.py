"""Declares :class:`ExternalIdentifierPrincipal`."""
from .principal import Principal


class ExternalIdentifierPrincipal(Principal):
    """Represents an identifier that is external."""
    platform = None

    def inrealm(self, realm):
        """Return a string holding an identifier within a realm."""
        assert self.platform is not None
        return f'realm+sso://{self.platform}@{realm}/{self.value}'

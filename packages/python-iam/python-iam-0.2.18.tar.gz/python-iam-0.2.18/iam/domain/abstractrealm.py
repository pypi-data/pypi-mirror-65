

class AbstractRealm:
    """Abstract implementation of an authorization realm."""

    def get_principal_roles(self, principal):
        """Return an iterable yielding the roles that were
        assigned to the principal in this realm.
        """
        raise NotImplementedError

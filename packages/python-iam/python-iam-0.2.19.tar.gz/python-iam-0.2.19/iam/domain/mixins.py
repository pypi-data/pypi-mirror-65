

class Authorizable:
    """Represents an object that is authorizable."""

    @classmethod
    def get_resource_class(cls):
        """Returns the resource class of the objec."""
        raise NotImplementedError

    def get_resource_qualname(self):
        """Returns the qualified name of a resource,
        identifying it within the global scope of
        a system.
        """
        raise NotImplementedError

    def get_subject_authorizations(self, subject):
        """Return a set holding the authorizations that
        the subject has on this entity. The default
        implementation returns an empty set, meaning
        no permissions.
        """
        realm = self.get_realm()
        return (
            self.get_resource_qualname(),
            realm.get_realm_authorizations(subject, self)\
            if realm else set()
        )

    def get_realm(self):
        """Returns the authorization realm to which this
        resource belongs.
        """
        raise NotImplementedError

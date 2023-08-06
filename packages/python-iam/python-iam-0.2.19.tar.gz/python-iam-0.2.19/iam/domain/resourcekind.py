

class ResourceKind(str):

    @classmethod
    def fromdjango(cls, obj):
        """Create a new :class:`ResourceKind` object
        from a Django model class or instance.
        """
        meta = obj._meta
        return cls(f'{meta.app_label}.{meta.object_name}')

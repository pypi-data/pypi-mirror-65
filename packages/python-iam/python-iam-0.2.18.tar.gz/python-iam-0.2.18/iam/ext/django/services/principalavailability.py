from django.apps import apps


class PrincipalAvailabilityService:

    def isavailable(self, realm, principal):
        """Return a bool indicating if the :term:`Principal` is available to
        add as an identifier for a :term:`Subject`.

        Args:
            principal (:class:`~iam.ext.domain.Principal`): the
                :term:`Principal` to identify a :term:`Subject` with.

        Returns:
            :obj:`bool`
        """
        Principal = apps.get_model('iam.Principal')
        return not Principal.objects.filter(
            realm_id=realm,
            kind=Principal.storage_kinds[principal.kind],
            value=principal.value
        ).exists()

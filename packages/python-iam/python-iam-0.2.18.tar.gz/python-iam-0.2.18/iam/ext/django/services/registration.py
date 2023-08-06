"""Declares :class:`RegistrationService`."""
import ioc
from django.apps import apps
from django.db import transaction


class RegistrationService:
    """Provides an interface to register new :term:`Subjects`."""
    availability = ioc.class_property('PrincipalAvailabilityService')

    def register(self, host, platform, realm, principal, credentials=None):
        """Register a new :term:`Subject`, that is identified by the given
        :term:`Principal` `principal` and authenticates with the
        :term:`Credentials` `credentials`. Return an :class:`uuid.UUID` that
        identifies the :term:`Subject`.
        """
        if not self.availability.isavailable(realm, principal):
            raise ValueError(
                f"{principal.kind}:{principal.value} is already associated.")
        Subject = apps.get_model('iam.Subject')
        SubjectRegistration = apps.get_model('iam.SubjectRegistration')
        with transaction.atomic():
            obj = Subject.objects.create(realm_id=realm)
            for credential in (credentials or []):
                obj.addcredential(credential)
            SubjectRegistration.objects.create(
                using_id=obj.addprincipal(principal),
                host=host,
                platform=platform
            )
        return obj.pk

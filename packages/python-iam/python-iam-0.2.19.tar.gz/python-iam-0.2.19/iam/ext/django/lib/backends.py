"""Declares authentication backends for the :mod:`iam.ext.django` Django
application.
"""
import ioc
from django.core.cache import cache
from unimatrix.lib import timezone

from iam.domain import PhonenumberPrincipal
from iam.ext.django.models import Subject


CHALLENGED_SESSION_KEY = 'iam:challenged'


class LocalSubjectBackend:
    model = Subject
    registration = ioc.class_property('RegistrationService')

    def authenticate(self, request, realm, principal, credential, **kwargs):
        """Authenticate a :term:`Subject` using the provided :term:`Principal`
        and :term:`Credential`.
        """
        try:
            subject = principal.resolve(realm, self.get_resolver())
        except self.model.DoesNotExist:
            credential.cooldown()
            return None
        else:
            if subject.check_credential(credential)\
            and self.can_authenticate(subject):
                return subject

    def can_authenticate(self, subject):
        """Return a boolean indicating if a :term:`Subject` may
        authenticate.
        """
        return True

    def get_user(self, subject_id):
        """Return a :class:`Subject` instance using the given `subject_id`."""
        return self.model.objects.get(pk=subject_id)

    def get_resolver(self):
        """Return an instance that can resolve a :class:`~iam.domain.Principal`."""
        return self.model.objects


class PhonenumberBackend(LocalSubjectBackend):
    """An authentication backend that allows authentication using a phone
    number combined with a password, PIN or confirmation code.
    """
    cache_lifetime = 3600

    def authenticate(self, request, realm, phonenumber, **kwargs):
        """Authenticate a :term:`Subject` using a phonenumber. If a confirmation
        code was sent, this may also create a new account.
        """
        subject = None
        if phonenumber is None:
            raise TypeError("`phonenumber` is a mandatory argument.")
        if kwargs.get('code'):
            subject = self.authenticate_using_code(
                request, PhonenumberPrincipal, phonenumber, kwargs['code'])
        elif kwargs.get('pin'):
            raise NotImplementedError
        elif kwargs.get('password'):
            raise NotImplementedError

        return subject

    def authenticate_using_code(self, request, principal_class, value, code):
        """Authenticate a :term:`Subject` using a One Time Password (OTP) sent
        over a secondary channel, such as SMS or email. If no :class:`Subject`
        exists, it may be created.
        """
        # Get the challenge from the cache. Bail out if there is no challenge.
        must_delete = False
        k = f'challenge:{value}'
        challenge = cache.get(k)
        if challenge is None:
            return None

        # Confirm the OTP and remove the challenge if the maximum attempts
        # are reached or it is valid.
        try:
            is_valid = challenge.confirm(code)
            if is_valid:
                must_delete = True
        except challenge.MaximumAttemptsReached:
            must_delete = True
            is_valid = False

        # Ensure that the code is deleted so it can not be reused.
        if must_delete:
            cache.delete(k)

        # Bail out if the provided code was not valid.
        if not is_valid:
            # Update the cache with the new state.
            if not must_delete:
                cache.set(k, challenge, self.cache_lifetime)
            return None

        # Instantiate a Principal object from the provided keyword arguments
        # and resolve it. If it doesn't exist, create it.
        created = False
        principal = principal_class(value)
        try:
            subject = principal.resolve('default', self.get_resolver())
        except self.model.DoesNotExist:
            pk = self.registration.register(
                request.host, request.site.domain, 'default', principal)
            subject = self.get_user(pk)
            created = True

        return subject

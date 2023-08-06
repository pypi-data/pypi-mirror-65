"""Declares the :class:`Subject` database object."""
import uuid

import ioc
from django.conf import settings
from django.utils.crypto import salted_hmac
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import is_password_usable
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from iam.lib.meta import AttributeDispatcher
from .platformagreements import PlatformAgreement
from .realms import Realm
from .passwordcredentials import PasswordCredential
from .permissionsmixin import PermissionsMixin


class Subject(AbstractBaseUser, PermissionsMixin):
    """A :class:`Subject` represents the source of a request to a system."""
    REQUIRED_FIELDS = ['realm']
    USERNAME_FIELD = 'id'
    credentials = ioc.class_property('CredentialService')
    storage_kinds = {
        'iam.unimatrixone.io/v1/FacebookAccountPrincipal': 'id.iam.unimatrixone.io/facebook',
        'iam.unimatrixone.io/v1/EmailPrincipal': 'id.iam.unimatrixone.io/email',
        'iam.unimatrixone.io/v1/GoogleAccountPrincipal': 'id.iam.unimatrixone.io/google',
        'iam.unimatrixone.io/v1/LinkedInAccountPrincipal': 'id.iam.unimatrixone.io/linkedin',
        'iam.unimatrixone.io/v1/NullPrincipal': 'id.iam.unimatrixone.io/null',
        'iam.unimatrixone.io/v1/PhonenumberPrincipal': 'id.iam.unimatrixone.io/phonenumber',
        'iam.unimatrixone.io/v1/TwitterAccountPrincipal': 'id.iam.unimatrixone.io/twitter',
    }

    # Remove properties that we don't want.
    password = last_login = None

    #: Maps :term:`Subject Properties` to related names.
    property_map = {
        'iam.unimatrixone.io/first-name'    : 'stringproperties',
        'iam.unimatrixone.io/last-name'     : 'stringproperties',
        'iam.unimatrixone.io/superuser'     : 'booleanproperties'
    }

    #: Indicates if the :class:`Subject` is authenticated. This attribute is
    #: always ``True``.
    is_authenticated = True

    #: Inverse of :attr:`is_authenticated`. This attribute is always ``False``.
    is_anonymous = False

    #: Specifies the :class:`~iam.ext.django.models.Realm` to which the
    #: :term:`Subject` belongs.
    realm = models.ForeignKey(
        Realm,
        on_delete=models.PROTECT,
        default=settings.IAM_REALM,
        blank=False,
        null=False,
        db_column='realm_name'
    )

    id = models.UUIDField(
        primary_key=True,
        blank=False,
        null=False,
        default=uuid.uuid4,
        db_column='id'
    )

    kind = models.CharField(
        max_length=63,
        blank=False,
        null=False,
        default='User',
        db_column='kind'
    )

    @property
    def first_name(self):
        return self._get_property('iam.unimatrixone.io/first-name')

    @first_name.setter
    def first_name(self, value):
        self._set_property('iam.unimatrixone.io/first-name', value)

    @property
    def is_active(self):
        return True

    @property
    def last_name(self):
        return self._get_property('iam.unimatrixone.io/last-name')

    @last_name.setter
    def last_name(self, value):
        self._set_property('iam.unimatrixone.io/last-name', value)

    @property
    def is_staff(self):
        return self.realm_id == settings.IAM_STAFF_REALM

    @property
    def is_superuser(self):
        return self._get_property('iam.unimatrixone.io/superuser')

    def accepts(self, agreement):
        """Return a boolean indicating if the :term:`Subject` accepted the
        :term:`Platform Agreement` `agreement`.
        """
        latest = PlatformAgreement.objects.effective(slug=agreement)
        qs = latest.languages.filter(accepted__subject__pk=self.pk)
        return qs.exists()

    def addcredential(self, credential):
        """Adds a :term:`Credential` to a :term:`Subject`.

        Args:
            credential (:class:`~iam.domain.Credential`): a credential
                implementation that the :term:`Subject` may use to prove its
                identity.

        Returns:
            :class:`types.NoneType`
        """
        assert type(credential).__name__ == 'PasswordCredential'
        dao, created = PasswordCredential.objects.get_or_create(
            subject=self, value=credential.secret
        )
        if not created:
            dao.value = credential.secret
            dao.save(update_fields=['value'])

    def addprincipal(self, principal):
        """Add a :term:`Principal` to the :term:`Subject`.

        Args:
            principal (:obj:`~iam.domain.Principal`): the :term:`Principal`
                to identify the :term:`Subject` with.

        Returns:
            :class:`types.NoneType`
        """
        return self.principals.create(kind=self.storage_kinds[principal.kind],
            value=principal.value).pk

    def check_credential(self, credential):
        """Verfifies the :term:`Credential` using the configured credential
        verification service.
        """
        if not credential:
            return False

        return self.credentials.verify(credential, self)

    def haspassword(self):
        """Return a boolean indicating if the :term:`Subject` has a
        :term:`Valid Password`.
        """
        try:
            self.password
            return True
        except (AttributeError, ObjectDoesNotExist):
            return False

    def hasprincipal(self, principal):
        """Return a boolean indicating if the :term:`Subject` is identified
        by the given :term:`Principal`.

        Args:
            principal (:class:`~iam.domain.Principal`): the :term:`Principal`
                to lookup.

        Returns:
            :obj:`bool`
        """
        return self.principals.filter(
            kind=self.storage_kinds[principal.kind],
            value=principal.value).exists()

    def marksuperuser(self, enabled):
        """Marks the :term:`Subject` as a :term:`Super User`."""
        kind = 'iam.unimatrixone.io/superuser'
        self._set_property(kind, enabled)

    # The methods below override some Django behavior.
    def has_usable_password(self):
        """Return False if set_unusable_password() has been called for
        this user.
        """
        try:
            return is_password_usable(self.password.value)
        except ObjectDoesNotExist:
            return False

    def get_full_name(self):
        """Return a string holding the full name for this :term:`Subject`."""
        return f'{self.first_name} {self.last_name}'

    def get_session_auth_hash(self):
        """Return a HMAC of the password; used to invalidate sessions by
        Django.
        """
        # This method is overridden because Django expects the password attribute
        # to always have a value. In the IAM application access of this attribute
        # may cause RelatedObjectDoesNotExist.
        key_salt = "iam.ext.django.models.Subject.get_session_auth_hash"
        try:
            return salted_hmac(key_salt, self.password.value).hexdigest()
        except ObjectDoesNotExist:
            return salted_hmac(key_salt, '').hexdigest()

    def __str__(self):
        return str(self.pk)

    class SubjectManager(models.Manager):

        def resolve(self, realm, principal):
            """Return a :class:`Subject` instance using a
            :class:`~iam.domain.Principal`.
            """
            return self.get_by_principal(realm, principal)

        def get_by_principal(self, realm, principal):
            """Return a :class:`Subject` instance using a
            :class:`~iam.domain.Principal`.
            """
            return self.get(
                realm__name=realm,
                principals__value=principal.value,
                principals__kind=self.model.storage_kinds[principal.kind])

    objects = SubjectManager()

    class Meta:
        app_label = 'iam'
        db_table = 'subjects'
        default_permissions = []

    def _get_property(self, kind):
        try:
            related_name = self.property_map[kind]
            return getattr(self, related_name).get(kind=kind).value
        except ObjectDoesNotExist:
            return None

    def _set_property(self, kind, value):
        manager = getattr(self, self.property_map[kind])
        try:
            dao = manager.get(kind=kind)
            dao.value = value
            dao.save(update_fields=['value'])
        except ObjectDoesNotExist:
            manager.create(kind=kind, value=value)

"""Declares the :class:`Realm` model."""
from django.db import models
from django.conf import settings

from iam.canon.dto import RealmConfigSchema



class Realm(models.Model):
    """A :class:`Realm` manages a set of users, credentials, roles, and groups.
    A :term:`Subject` belongs to and logs into a :term:`Realm`. Realms are
    isolated from one another and can only manage and authenticate the users
    that they control.
    """

    @property
    def config(self):
        schema = RealmConfigSchema()
        return schema.load(settings.IAM_REALM_SETTINGS.get(self.name) or {})

    #: A symbolic name for the realm. The :attr:`name` attribute may consist
    #: of alphanumeric characters and start with a letter. It can not be changed
    #: after creating the realm.
    name = models.CharField(
        max_length=64,
        primary_key=True,
        blank=False,
        null=False,
        db_column='name'
    )

    #: A human-readable name for the realm.
    label = models.CharField(
        max_length=64,
        blank=False,
        null=False,
        db_column='label'
    )

    def allowsso(self, provider):
        """Return a boolean indicating if this :term:`Realm` allow
        authentication using the specified SSO `provider`.
        """
        return provider in self.config.sso.providers

    def getssoproviders(self):
        """Return a tuple containg all SSO providers for this realm."""
        return tuple(self.config.sso.providers)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'iam'
        db_table = 'realms'
        default_permissions = []

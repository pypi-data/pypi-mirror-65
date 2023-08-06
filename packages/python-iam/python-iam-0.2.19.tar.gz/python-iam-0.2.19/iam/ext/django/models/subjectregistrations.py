"""Declares :class:`SubjectRegistration`."""
from django.db import models
from django.utils.translation import gettext as _

import unimatrix.lib.timezone


class SubjectRegistration(models.Model):
    """Maintains information about the registration of a :term:`Subject`."""

    #: The :term:`Principal` that the :term:`Subject` or its :term:`Registrar`
    #: used to create the account.
    using = models.OneToOneField(
        'iam.Principal',
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        primary_key=True,
        db_column='principal_id'
    )

    #: The host address from which the :term:`Subject` was registered.
    host = models.GenericIPAddressField(
        blank=False,
        null=False,
        db_column='host'
    )

    #: Identifies the platform through which the :term:`Subject` registered.
    platform = models.CharField(
        max_length=127,
        blank=False,
        null=False,
        db_column='platform'
    )

    #: Identifies the entity that registered the :term:`Subject`. The value
    #: ``self`` indicates that the :term:`Subject` registered on its own
    #: behalf (e.g. through a publicly accessible web interface).
    registrar = models.CharField(
        max_length=127,
        default='self',
        blank=False,
        null=False,
        db_column='registrar'
    )

    #: The date/time at which the :term:`Subject` was registered, in
    #: milliseconds since the UNIX epoch.
    timestamp = models.BigIntegerField(
        default=unimatrix.lib.timezone.now,
        blank=False,
        null=False,
        db_column='timestamp'
    )

    #: Two zero octets followed by the DER-encoded response of a trusted
    #: :term:`Time Stamping Authority` (TSA) compliant to the :rfc:`3161`
    #: `Internet X.509 Public Key Infrastructure Time-Stamp Protocol (TSP)`
    #: specification.
    #:
    #: The ``hashedMessage`` is a SHA-256 hash consisting of the following
    #: data-elements:
    #:
    #: - :attr:`~iam.ext.django.models.Principal.subject_id` (from :attr:`using`)
    #: - :attr:`~iam.ext.django.models.Principal.kind` (from :attr:`using`)
    #: - :attr:`~iam.ext.django.models.Principal.value` (from :attr:`using`)
    #: - :attr:`host`
    #: - :attr:`using`
    #: - :attr:`registrar`
    #: - :attr:`timestamp`
    #:
    #: Since it is not assumed that a highly-available :term:`TSA` is deployed
    #: in every scenario, this field initializes to an empty byte-sequence and
    #: is processed asynchronously. Implementations should take care to ensure
    #: that the field is updated as soon as possible after registration. This
    #: may be done using the ``python manage.py updateregistrationtsrs``.
    tsr = models.BinaryField(
        default=bytes,
        blank=False,
        null=False,
        db_column='tsr'
    )

    class Meta:
        app_label = 'iam'
        db_table = 'subjectregistrations'
        default_permissions = []
        verbose_name = _("Registration")
        verbose_name_plural = _("Registrations")

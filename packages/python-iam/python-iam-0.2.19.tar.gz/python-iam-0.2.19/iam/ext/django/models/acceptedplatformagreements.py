"""Declares :class:`AcceptedPlatformAgreement`."""
import hashlib

from django.db import models
from django.utils.translation import gettext_lazy as _
from unimatrix.lib import timezone


class AcceptedPlatformAgreement(models.Model):
    """Maintains information about :term:`Platform Agreements` that are
    accepted by a :term:`Subject`.
    """

    #: The :class:`~iam.ext.django.models.PlatformAgreementLanguage` that
    #: was accepted by :attr:`subject`.
    agreement = models.ForeignKey(
        'iam.PlatformAgreementLanguage',
        to_field='checksum',
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        related_name='accepted',
        db_column='agreement_checksum'
    )

    #: The :class:`~iam.ext.django.models.Subject` that accepted
    #: :attr:`agreement`.
    subject = models.ForeignKey(
        'iam.Subject',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='agreements',
        db_column='subject_id'
    )

    #: The host address from which the :attr:`agreement` was accepted.
    host = models.GenericIPAddressField(
        blank=False,
        null=False,
        db_column='host'
    )

    #: The date/time at which the :attr:`agreement` was accepted, in
    #: milliseconds since the UNIX epoch.
    timestamp = models.BigIntegerField(
        default=timezone.now,
        blank=False,
        null=False,
        db_column='timestamp'
    )

    #: A SHA-256 hash of :attr:`content`.
    checksum = models.CharField(
        max_length=128,
        blank=False,
        null=False,
        editable=False,
        unique=True,
        db_column='checksum'
    )

    def generate_checksum(self):
        """Make a checksum of the agreements' content."""
        h = hashlib.sha256()
        h.update(str.encode(self.agreement_id))
        h.update(self.subject_id.bytes)
        h.update(int.to_bytes(self.timestamp, 8, 'big'))
        h.update(str.encode(self.host))
        return h.hexdigest()

    def save(self, *args, **kwargs):
        """Ensure that the :attr:`checksum` field is updated and proceed to
        persist the entity.
        """
        if not self._state.adding:
            raise ValueError("AcceptedPlatformAgreement objects are immutable.")
        self.checksum = self.generate_checksum()
        update_fields = kwargs.get('update_fields')
        if update_fields:
            update_fields.append('checksum')
        return super().save(*args, **kwargs)

    class Meta:
        app_label = 'iam'
        db_table = 'acceptedplatformagreements'
        default_permissions = []
        unique_together = ['agreement', 'subject']
        verbose_name = _('Accepted Platform Agreement')
        verbose_name_plural = _('Accepted Platform Agreements')

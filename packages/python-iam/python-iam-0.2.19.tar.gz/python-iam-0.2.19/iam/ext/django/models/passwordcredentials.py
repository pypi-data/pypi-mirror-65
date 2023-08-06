"""Declares :class:`PasswordCredential`."""
from django.db import models


class PasswordCredential(models.Model):
    """Maintains hashed passwords and basic properties, such as an expiration
    date.
    """
    subject = models.OneToOneField(
        'iam.Subject',
        on_delete=models.CASCADE,
        primary_key=True,
        blank=False,
        null=False,
        related_name='password',
        db_column='subject_id'
    )

    value = models.CharField(
        max_length=128,
        blank=False,
        null=False,
        db_column='value'
    )

    class Meta:
        app_label = 'iam'
        db_table = 'passwordcredentials'
        default_permissions = []

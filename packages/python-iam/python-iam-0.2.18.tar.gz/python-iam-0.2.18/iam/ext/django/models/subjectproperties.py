"""Declares :class:`SubjectProperty`."""
from django.db import models


class SubjectProperty(models.Model):
    """Specifies the abstract interface for :term:`Subject Properties`."""

    id = models.BigAutoField(
        primary_key=True,
        blank=False,
        null=False,
        db_column='id'
    )

    subject = models.ForeignKey(
        'iam.Subject',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        db_column='subject_id'
    )

    kind = models.CharField(
        max_length=127,
        blank=False,
        null=False,
        db_column='kind'
    )

    class Meta:
        abstract = True

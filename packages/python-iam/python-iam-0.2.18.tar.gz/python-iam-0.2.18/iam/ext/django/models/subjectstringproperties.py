"""Declares :class:`SubjectStringProperty`."""
from django.db import models

from .subjectproperties import SubjectProperty


class SubjectStringProperty(SubjectProperty):
    """Maintains a :term:`Subject Property` of type :obj:`str`.

    Attributes:
        value (:obj:`str`): the value of the :term:`Subject Property`.
    """
    value = models.CharField(
        max_length=127,
        blank=False,
        null=False,
        db_column='value'
    )

    class Meta:
        app_label = 'iam'
        db_table = 'subjectstringproperties'
        default_permissions = []
        default_related_name = 'stringproperties'
        unique_together = ['subject', 'kind']

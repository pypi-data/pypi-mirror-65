"""Declares :class:`SubjectBooleanProperty`."""
from django.db import models

from .subjectproperties import SubjectProperty


class SubjectBooleanProperty(SubjectProperty):
    """Maintains a :term:`Subject Property` of type :obj:`str`.

    Attributes:
        value (:obj:`str`): the value of the :term:`Subject Property`.
    """
    value = models.BooleanField(
        blank=False,
        null=False,
        db_column='value'
    )

    class Meta:
        app_label = 'iam'
        db_table = 'subjectbooleanproperties'
        default_permissions = []
        default_related_name = 'booleanproperties'
        unique_together = ['subject', 'kind']

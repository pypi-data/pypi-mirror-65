"""Declares :class:`SubjectRepository`."""
from django.apps import apps


class SubjectRepository:
    """Provides an interface to lookup :class:`~iam.ext.django.models.Subject`
    Data Access Objects (DAOs).
    """

    @property
    def model(self):
        return apps.get_model('iam.Subject')

    def get(self, pk):
        """Look up a :term:`Subject` by its identifier."""
        return self.model.objects.get(pk=pk)

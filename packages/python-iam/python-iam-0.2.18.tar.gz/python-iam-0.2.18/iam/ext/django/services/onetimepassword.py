"""Declares :class:`OneTimePasswordService`."""
import ioc
from django.apps import apps
from unimatrix.lib import timezone


class OneTimePasswordService:
    """Provides an interface to generate and verify :term:`One Time Password`
    instances for a :term:`Subject`.
    """

    @property
    def model(self):
        return apps.get_model('iam.LoginCode')

    def generate(self, subject):
        """Generate a new :term:`One Time Password` for the :term:`Subject`
        identified by UUID `subject`. Return a boolean indicating if a new
        code was created.

        Args:
            subject (:class:`uuid.UUID`): identifies the :term:`Subject` to
                generate a code for.

        Returns:
            :obj:`bool`
        """
        # Ensure that expired login codes are deleted.
        self.model.objects.filter(subject=subject,
            generated__lte=(timezone.now() - self.model.MIN_LIFETIME)).delete()
        obj, created = self.model.objects.get_or_create(subject=subject)
        return obj.code

    def verify(self, subject, code):
        """Verify that `code` is valid for the given `subject`.

        Args:
            subject (:class:`uuid.UUID`): identifies the :term:`Subject` to
                verify a code for.
            code (:obj:`str`): the code to verify.

        Returns:
            :obj:`bool`
        """
        try:
            dao = self.model.objects.get(subject=subject)
        except self.model.DoesNotExist:
            return False
        return dao.verify(code)

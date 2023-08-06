"""Declares :class:`PasswordService`."""
import ioc
from django.apps import apps

from iam.domain import PasswordCredential


class PasswordService:
    """Exposes an interface to change and expire passwords."""
    repo = ioc.class_property('SubjectRepository')

    def change(self, subject, password):
        """Change the password for :term:`Subject` `subject`.

        Args:
            subject (:class:`uuid.UUID`): identifies the :term:`Subject` to
                generate a code for.
            password (:obj:`str`): the new password to set for the
                :term:`Subject`.

        Returns:
            :class:`types.NoneType`
        """
        subject = self.repo.get(subject)
        subject.addcredential(PasswordCredential(password))

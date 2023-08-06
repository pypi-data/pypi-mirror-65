from django.apps import apps


class HashedPasswordRepository:

    @property
    def model(self):
        return apps.get_model('iam.PasswordCredential')

    def get(self, subject):
        """Returns the hashed password that may be used to authenticate
        the given :term:`Subject` `subject`.

        Args:
            subject (:obj:`str`): the :term:`Subject Identifier` to look up
                the password for.

        Returns:
            :obj:`str` or ``None`` if the :term:`Subject` does not have a
            password.
        """
        try:
            return self.model.objects.get(subject_id=subject)
        except self.model.DoesNotExist:
            return None

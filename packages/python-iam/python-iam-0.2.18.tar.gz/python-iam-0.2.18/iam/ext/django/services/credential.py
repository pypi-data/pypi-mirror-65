"""Declares :class:`CredentialService`."""
import ioc

from iam.lib.meta import AttributeDispatcher


class CredentialService:
    """Provides an interface to verify and update credentials for specific
    :term:`Subjects`.
    """
    passwords = ioc.class_property('HashedPasswordRepository')
    otp = ioc.class_property('OneTimePasswordService')

    @AttributeDispatcher.dispatch('kind')
    def verify(self, func, credential, subject):
        return func(credential, subject)

    @verify.register('iam.unimatrixone.io/v1/PasswordCredential')
    def verify(self, credential, subject):
        secret = self.passwords.get(subject)
        return credential.check(secret.value)\
            if secret is not None\
            else False

    @verify.register('iam.unimatrixone.io/v1/LoginCodeCredential')
    def verify(self, credential, subject):
        return self.otp.verify(subject.pk, credential.secret)

    @verify.register('iam.unimatrixone.io/v1/NullCredential')
    def verify(self, credential, subject):
        return False

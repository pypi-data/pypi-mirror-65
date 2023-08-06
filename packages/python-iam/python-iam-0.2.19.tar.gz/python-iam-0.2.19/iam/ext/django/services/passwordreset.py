"""Declares class:`PasswordResetService`."""
import ioc
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext as _

import iam.lib.urls
from iam.lib.meta import AttributeDispatcher


class PasswordResetService:
    """Exposes an interface to reset passwords."""
    otp = ioc.class_property('OneTimePasswordService')
    template = ioc.class_property('iam.TemplateService')

    @AttributeDispatcher.dispatch('kind')
    def challenge(self, func, principal):
        return func(principal)

    @challenge.register('iam.unimatrixone.io/v1/EmailPrincipal')
    def challenge(self, principal, verify=None, context_data=None):
        """Challenge the :term:`Subject` by sending a :term:`One Time Password`
        to the :term:`Principal`. Return a boolean indicating if a challenge
        was sent.

        Args:
            principal (:class:`~iam.domain.Principal`): the :term:`Principal`
                to send the :term:`One Time Password` to. It must be a valid
                :term:`Contact Mechanism`.
            verify (:obj:`str`): a string holding an URL that the
                :term:`Subject` may visit to continue the password reset
                process.

        Returns:
            :obj:`bool`
        """
        try:
            principal.subject.password.delete() # TODO: move to PasswordService
        except (AttributeError, ObjectDoesNotExist):
            pass
        code = self.otp.generate(principal.subject.pk)
        ctx = context_data or {}

        # Append the code to the URI so that the endpoint can detect is.
        if verify:
            verify = iam.lib.urls.updateqs(verify, {
                'token': code,
                'principal': principal.value
            })

        ctx.update({
            'principal': principal,
            'subject': principal.subject,
            'code': code,
            'url': verify
        })

        principal.send(
            subject=_("Reset your password"),
            text=self.template.render_to_string('email/resetpassword.body.txt.j2', ctx))

    def verify(self, subject, code):
        """Verify that the given `code` matches the one sent in the challenge.
        If `code` is valid, mark the :term:`Password` associated to the
        :term:`Subject` as expired, so it will be forced to choose a new one,
        and return a boolean indicating if the code verification was a succes.

        Args:
            subject (:class:`uuid.UUID`): a Universally Unique Identifier (UUID)
                identifying the :term:`Subject` that was challenged.
            code (:obj:`str`): the secret that was sent to the :term:`Subject`.

        Returns:
            :obj:`bool`
        """
        return False

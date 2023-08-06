"""Declares :class:`LoginCode`."""
import django.utils.crypto
from django.db import models

from unimatrix.lib import timezone

import iam.domain


class LoginCode(models.Model):
    """Maintains information about one-time login codes.

    Attributes:
        subject (:class:`~iam.ext.django.models.Subject`): the
            :term:`Subject` for which the code is used to authenticate.
        code (:obj:`str`): the temporary login code.
        attempts (:obj:`int`): number of attempts to authenticate on the
            :attr:`subject`.
        generated (:obj:`int`): the date/time at which the code was generated,
            in milliseconds since the UNIX epoch.
    """
    MAX_ATTEMPTS = 5

    #: Minimum lifetime of the login code, in milliseconds. A new  code is
    #: not generated before :attr:`MIN_LIFETIME` is expired (based on the
    #: value of :attr:`generated`).
    MIN_LIFETIME = 1000 * 60 * 10

    subject = models.UUIDField(
        primary_key=True,
        blank=False,
        null=False,
        db_column='subject'
    )

    code = models.CharField(
        max_length=127,
        default=iam.domain.LoginCode.new,
        blank=False,
        null=False,
        db_column='code'
    )

    attempts = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
        db_column='attempts'
    )

    generated = models.BigIntegerField(
        default=timezone.now,
        blank=False,
        null=False,
        db_column='generated'
    )

    def verify(self, code):
        """Verify that `code` is correct and increase :attr:`attempts`. If the
        maximum attempts treshold is reached, delete the object.
        """
        # Delete the LoginCode if the maximum attempts is reached and the
        # minimum lifetime is expired.
        if (self.attempts >= self.MAX_ATTEMPTS):
            if (timezone.now() - self.generated) > self.MIN_LIFETIME:
                self.delete()
            return False
        isvalid = django.utils.crypto.constant_time_compare(code, self.code)
        if not isvalid:
            self.attempts = models.F('attempts') + 1
            self.save(update_fields=['attempts'])
            self.refresh_from_db()
        else:
            self.delete()
        return isvalid

    class Meta:
        app_label = 'iam'
        db_table = 'logincodes'
        default_permissions = []

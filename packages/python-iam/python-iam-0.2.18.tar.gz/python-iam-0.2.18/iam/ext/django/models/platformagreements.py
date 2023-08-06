"""Declares :class:`PlatformAgreement`."""
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class PlatformAgreement(models.Model):
    """Maintains a :term:`Agreement` for use of a system."""

    slug = models.SlugField(
        primary_key=True,
        blank=False,
        null=False,
        db_column='slug'
    )

    #: Human-readable title of the :term:`Platform Agreement`.
    title = models.CharField(
        max_length=127,
        blank=False,
        null=False,
        db_column='title'
    )

    #: The date/time at which the :term:`Platform Agreement` becomes
    #: effective.
    effective = models.DateTimeField(
        blank=False,
        null=False,
        db_column='effective'
    )

    def iseffective(self):
        """Return a boolean indicating if the :term:`Platform Agreement`
        is effective.
        """
        return self.effective <= timezone.now()

    class PlatformAgreementManager(models.Manager):

        def effective(self, slug):
            """Return the :term:`Effective Platform Agreement`, identified by
            the given `slug`.
            """
            return self.filter(slug=slug).order_by('-effective')[:1].get()

    objects = PlatformAgreementManager()

    class Meta:
        app_label = 'iam'
        db_table = 'platformagreements'
        default_permissions = []
        ordering = ['-effective']
        verbose_name = _("Platform Agreement")
        verbose_name_plural = _("Platform Agreements")

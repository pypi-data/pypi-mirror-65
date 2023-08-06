"""Declares :class:`PlatformAgreementLanguage`."""
import hashlib

import markdown
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language


class PlatformAgreementLanguage(models.Model):
    """A :term:`Platform Agreement` in a specific language."""

    agreement = models.ForeignKey(
        'iam.PlatformAgreement',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='languages',
        db_column='agreement_slug'
    )

    #: A SHA-256 hash of :attr:`content`.
    checksum = models.CharField(
        max_length=128,
        blank=False,
        null=False,
        editable=False,
        unique=True,
        db_column='checksum'
    )

    #: The language in which :attr:`content` is written.
    language = models.CharField(
        max_length=15,
        blank=False,
        null=False,
        choices=tuple(settings.LANGUAGES),
        db_column='language'
    )

    #: The encoding of :attr:`content`
    encoding = models.CharField(
        max_length=31,
        default='utf-8',
        blank=False,
        null=False,
        editable=False,
        db_column='encoding'
    )

    #: The markup language of :attr:`content`.
    markup = models.CharField(
        max_length=31,
        default='markdown',
        blank=False,
        null=False,
        editable=False,
        db_column='markup'
    )

    #: The title of the translated agreemend.
    title = models.CharField(
        max_length=127,
        blank=False,
        null=False,
        db_column='title'
    )

    #: The content of the translated agreement.
    content = models.TextField(
        blank=False,
        null=False,
        db_column='content'
    )

    def generate_checksum(self):
        """Make a checksum of the agreements' content."""
        h = hashlib.sha256()
        h.update(str.encode(self.agreement_id))
        h.update(str.encode(self.language))
        h.update(str.encode(self.title, self.encoding))
        h.update(str.encode(self.content, self.encoding))
        return h.hexdigest()

    def has_agreements(self):
        """Return a boolean indicating if the :term:`Platform Agreement`
        has agreements from :term:`Subjects` in :attr:`language`.
        """
        return False

    def render(self):
        """Renders :attr:`content` in the specified :attr:`markup`."""
        assert self.markup == 'markdown'
        return markdown.markdown(self.content)

    def save(self, *args, **kwargs):
        """Ensure that the :attr:`checksum` field is updated and proceed to
        persist the entity.
        """
        if self.has_agreements():
            raise ValueError(
                "Can not modify agreements to which Subjects consented.")
        self.checksum = self.generate_checksum()
        update_fields = kwargs.get('update_fields')
        if update_fields:
            # Assume this is a list.
            update_fields.append('checksum')
        return super().save(*args, **kwargs)

    class PlatformAgreementLanguageManager(models.Manager):

        def get_effective(self, agreement, language=None):
            """Returns the :class:`PlatformAgreementLanguage` instance
            for the current language and specified :term:`Platform Agreement`
            `agreement`.
            """
            try:
                return self.get(
                    agreement_id=agreement,
                    agreement__effective__lte=timezone.now(),
                    language=language or get_language())
            except self.model.DoesNotExist:
                return self.get(
                    agreement_id=agreement,
                    agreement__effective__lte=timezone.now(),
                    language=settings.IAM_TERMS_AUTHORITATIVE_LANGUAGE)

    objects = PlatformAgreementLanguageManager()

    class Meta:
        app_label = 'iam'
        db_table = 'platformagreementlanguages'
        default_permissions = []
        verbose_name = _("Platform Agreement Translation")
        verbose_name_plural = _("Platform Agreements Translations")
        unique_together = ['agreement', 'language']

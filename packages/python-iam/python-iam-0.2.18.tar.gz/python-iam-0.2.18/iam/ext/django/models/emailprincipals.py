"""Declares :class:`~iam.ext.django.models.EmailPrincipal`."""
from django.db import models


class EmailPrincipal(models.Model):
    """Maintains an email address and associated properties for a :term:`Subject`
    within a :term:`Realm`.
    """

    #: Specifies the :class:`~iam.ext.django.models.Realm` to which the
    #: :term:`Email Principal` belongs.
    realm = models.ForeignKey(
        'iam.Realm',
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        db_column='realm_name'
    )

    #: Specifies the :term:`Subject` that is identified by the email address.
    subject = models.ForeignKey(
        'iam.Subject',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='email',
        db_column='subject_id'
    )

    value = models.EmailField(
        blank=False,
        null=False,
        db_column='value'
    )

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.realm_id = self.subject.realm_id
        return super().save(*args, **kwargs)

    class Meta:
        app_label = 'iam'
        db_table = 'emailprincipals'
        default_permissions = []

        #: TODO: Worst normalization ever. A both realms and subjects can not
        #: have duplicate emails, but no composite keys in Django FTW.
        unique_together = [
            ('realm', 'value'),
            ('subject', 'value')
        ]

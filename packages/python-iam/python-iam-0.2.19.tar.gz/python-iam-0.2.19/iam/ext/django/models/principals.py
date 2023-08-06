"""Declares :class:`~iam.ext.django.models.Principal`."""
from django.db import models


class Principal(models.Model):
    """Generic object that maintains :term:`Principals`."""

    #: Maps domain object type identifiers to internal storage identifiers.
    storage_kinds = {
        'iam.unimatrixone.io/v1/FacebookAccountPrincipal': 'id.iam.unimatrixone.io/facebook',
        'iam.unimatrixone.io/v1/EmailPrincipal': 'id.iam.unimatrixone.io/email',
        'iam.unimatrixone.io/v1/GoogleAccountPrincipal': 'id.iam.unimatrixone.io/google',
        'iam.unimatrixone.io/v1/LinkedInAccountPrincipal': 'id.iam.unimatrixone.io/linkedin',
        'iam.unimatrixone.io/v1/NullPrincipal': 'id.iam.unimatrixone.io/null',
        'iam.unimatrixone.io/v1/PhonenumberPrincipal': 'id.iam.unimatrixone.io/phonenumber',
        'iam.unimatrixone.io/v1/TwitterAccountPrincipal': 'id.iam.unimatrixone.io/twitter',
    }

    #: A surrogate primary key for this :term:`Principal`.
    id = models.BigAutoField(
        primary_key=True,
        blank=False,
        null=False,
        db_column='id'
    )

    #: Specifies the :class:`~iam.ext.django.models.Realm` to which the
    #: :term:`Principal` belongs.
    realm = models.ForeignKey(
        'iam.Realm',
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        db_column='realm_name'
    )

    #: Specifies the :term:`Subject` that is identified by the principal.
    subject = models.ForeignKey(
        'iam.Subject',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='principals',
        db_column='subject_id'
    )

    kind = models.CharField(
        max_length=64,
        blank=False,
        null=False,
        db_column='kind'
    )

    value = models.CharField(
        max_length=64,
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
        db_table = 'principals'
        default_permissions = []

        #: TODO: Worst normalization ever. A both realms and subjects can not
        #: have duplicate principals, but no composite keys in Django FTW.
        unique_together = [
            ('realm', 'kind', 'value'),
            ('subject', 'kind', 'value')
        ]


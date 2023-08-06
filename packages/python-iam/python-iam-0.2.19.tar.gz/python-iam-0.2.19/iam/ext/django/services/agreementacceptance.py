"""Declares :class:`AgreementAcceptanceService`."""
from django.apps import apps


class AgreementAcceptanceService:
    """Provides an interface to accept :term:`Platform Agreements`."""

    @property
    def model(self):
        return apps.get_model('iam.PlatformAgreementLanguage')

    def accept(self, checksum, subject, host):
        """Accepts the :term:`Platform Agreement` `oid` for a
        :term:`Subject`.

        Args:
            checksum (:obj:`int`): the checksum of the agreement to accept.
            subject (:obj:`uuid.UUID`): identifies the :term:`Subject`.
            host (:obj:`str`): the remote host address (IPv4/IPv6) from
                which the HTTP request to accept the agreement was made.

        Returns:
            :class:`types.NoneType`
        """
        AcceptedPlatformAgreement = apps.get_model(
            'iam.AcceptedPlatformAgreement')

        AcceptedPlatformAgreement.objects.create(agreement_id=checksum,
            subject_id=subject, host=host)

    def accepted(self, subject, terms):
        """Return a Data Transfer Object (DTO) holding the latest version of
        `terms` that `subject` accepted. If the :term:`Subject` did never
        accept these terms, return ``None``.
        """
        AcceptedPlatformAgreement = apps.get_model(
            'iam.AcceptedPlatformAgreement')
        qs = AcceptedPlatformAgreement.objects.filter(
            agreement__agreement__slug=terms, subject_id=subject)
        try:
            return qs.latest('timestamp')
        except AcceptedPlatformAgreement.DoesNotExist:
            return None

    def latest(self, language, terms):
        """Return a Data Transfer Object (DTO) holding the latest version
        of the specified `terms`.
        """
        return self.model.objects.get_effective(terms, language=language)

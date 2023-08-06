"""Declares context processors for use with Django."""
from django.conf import settings
from django.utils.functional import SimpleLazyObject

from iam.ext.django.models import PlatformAgreementLanguage


def policies(request):
    """Updates the context with the effective :term:`Terms of Service` and
    :term:`Privacy Policy`.
    """
    f = lambda: PlatformAgreementLanguage.objects.get_effective(
        settings.IAM_TERMS_OF_SERVICE)
    p = lambda: PlatformAgreementLanguage.objects.get_effective(
        settings.IAM_PRIVACY_POLICY)
    return {
        'iam_terms_of_service': SimpleLazyObject(f),
        'iam_privacy_policy': SimpleLazyObject(p)
    }


def context(request):
    """Adds common IAM context variables."""
    ctx = {
        'subject': request.user
    }
    ctx['iam_urls'] = {
        'forms': {
            'names': f'{settings.IAM_URL_NAMESPACE}:forms:names',
            'terms': f'{settings.IAM_URL_NAMESPACE}:forms:terms',
        },
        'login': f'{settings.IAM_URL_NAMESPACE}:login',
        'login_token': f'{settings.IAM_URL_NAMESPACE}:login.token',
        'logout': f'{settings.IAM_URL_NAMESPACE}:logout',
        'register': f'{settings.IAM_URL_NAMESPACE}:register',
        'resetcredentials': f'{settings.IAM_URL_NAMESPACE}:resetcredentials',
    }
    return ctx

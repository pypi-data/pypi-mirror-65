"""Declares :class:`PlatformAgreementLanguageAdmin`."""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from iam.ext.django.models import PlatformAgreementLanguage


class PlatformAgreementLanguageAdmin(admin.ModelAdmin):
    pass


admin.site.register(PlatformAgreementLanguage, PlatformAgreementLanguageAdmin)

"""Declares :class:`AcceptedPlatformAgreementAdmin`."""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ..models import AcceptedPlatformAgreement
from .readonly import ReadonlyModelAdminMixin


class AcceptedPlatformAgreementAdmin(ReadonlyModelAdminMixin, admin.ModelAdmin):
    list_filter = ['subject__realm']
    list_display = ['timestamp', 'title', 'host', 'first_name', 'last_name']

    def title(self, obj):
        return f'{obj.agreement.title} {obj.agreement.agreement.effective.date()}'
    title.short_description = _('Title')

    def first_name(self, obj):
        return obj.subject.first_name or ''
    first_name.short_description = _('First name')

    def last_name(self, obj):
        return obj.subject.last_name or ''
    last_name.short_description = _('Last name')


admin.site.register(AcceptedPlatformAgreement, AcceptedPlatformAgreementAdmin)

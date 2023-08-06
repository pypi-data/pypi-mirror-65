"""Declares :class:`SubjectRegistrationAdmin`."""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from iam.ext.django.models import SubjectRegistration
from .readonly import ReadonlyModelAdminMixin


class SubjectRegistrationAdmin(ReadonlyModelAdminMixin, admin.ModelAdmin):
    readonly = True
    search_fields = ['using__subject__stringproperties__value']
    list_filter = ['using__realm', 'registrar', 'platform']
    list_display = ['timestamp', 'realm', 'platform', 'registrar', 'using_short',
        'host', 'first_name', 'last_name']
    ordering = ['-timestamp']

    def using_short(self, obj):
        return str.split(obj.using.kind, '/')[-1]
    using_short.short_description = _('Using')

    def realm(self, obj):
        return obj.using.realm_id
    realm.short_description = _('Realm')

    def first_name(self, obj):
        return obj.using.subject.first_name or ''
    first_name.short_description = _('First name')

    def last_name(self, obj):
        return obj.using.subject.last_name or ''
    last_name.short_description = _('Last name')


admin.site.register(SubjectRegistration, SubjectRegistrationAdmin)

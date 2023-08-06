"""Declares :class:`AcceptAgreementFormView`."""
import ioc
from django import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.decorators import method_decorator

from .basepartialform import BasePartialFormView
from ..models import PlatformAgreementLanguage


@method_decorator(login_required, 'dispatch')
class AcceptAgreementFormView(BasePartialFormView):
    template_name = 'iam/includes/forms/login.completenames.html.j2'
    agreement = ioc.class_property('AgreementAcceptanceService')

    class form_class(forms.Form):
        agreement = forms.ModelChoiceField(
            required=True,
            queryset=PlatformAgreementLanguage.objects.all(),
            to_field_name='checksum'
        )

    def form_invalid(self, form):
        """Indicate the caller that the form is not valid."""
        return HttpResponse(status=422)

    def form_valid(self, form):
        """Mark the agreement as accepted."""
        self.agreement.accept(form.cleaned_data['agreement'].checksum,
            self.request.user.pk, self.request.host)
        return HttpResponse(status=201)

"""Declares :class:`ChooseNamesFormView`."""
from django import forms

from ..lib.forms import NameField
from .basepartialform import BasePartialFormView


class ChooseNamesFormView(BasePartialFormView):
    template_name = 'iam/includes/forms/login.completenames.html.j2'


    class form_class(forms.Form):
        first_name = NameField(
            required=True,
            max_length=32
        )

        last_name = NameField(
            required=True,
            max_length=32
        )

    def form_valid(self, form):
        """Update the :term:`Subject` with the given first and last name."""
        self.request.user.first_name = form.cleaned_data['first_name']
        self.request.user.last_name = form.cleaned_data['last_name']
        return super().form_valid(form)

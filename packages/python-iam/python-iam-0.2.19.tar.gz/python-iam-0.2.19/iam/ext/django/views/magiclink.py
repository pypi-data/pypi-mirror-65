"""Declares :class:`MagicLinkView`."""
from django import forms
from django.views.generic import FormView

from .login import LoginView


class MagicLinkView(LoginView):
    """Provides a mechanism to send a magic link for login purposes to
    known users.
    """
    template_name = 'iam/login.magic.html.j2'

    class form_class(forms.Form):
        email = forms.EmailField(
            required=True
        )

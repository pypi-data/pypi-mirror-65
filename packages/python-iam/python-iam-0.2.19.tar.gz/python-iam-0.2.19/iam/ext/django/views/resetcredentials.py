"""Declares :class:`ResetCredentialsView`."""
import ioc
from django.contrib.auth import logout
from django import forms
from django.views.generic import FormView

import iam.lib.urls
from .forms import BasePrincipalForm
from .subjectonboarding import SubjectOnboardingMixin


class ResetCredentialsView(SubjectOnboardingMixin, FormView):
    """Provides ``GET`` and ``POST`` request handlers to reset the credentials
    for an account.
    """
    reset = ioc.class_property('PasswordResetService')
    template_name = 'iam/resetcredentials.html.j2'

    class form_class(BasePrincipalForm):

        principal = forms.CharField(
            max_length=64,
            required=True
        )

        def get_user(self):
            """Returns the user found by the valid login credentials."""
            return self.subject

    def form_valid(self, form):
        """We found to user and can now continue the flow."""
        logout(self.request)
        principal, subject = form.get_principal(resolve=True)
        if subject is not None:
            self.reset.challenge(principal,
                verify=self.get_token_login_url(),
                context_data={
                    'brand_name': self.request.site.name or self.request.site.domain
                })
        return self.render_to_response(
            self.get_context_data(form=form, state='challenged')
        )

    def get_token_login_url(self):
        """Return the URL at which the :term:`Subject` can use the
        reset token.
        """
        uri = self.request.build_absolute_uri(
            iam.lib.urls.reverse('login.token'))
        if self.request.META['QUERY_STRING']:
            uri += f"?{self.request.META['QUERY_STRING']}"
        return uri

    def get_template_names(self):
        """Return a list of template names."""
        if self.request.method == 'GET':
            return super().get_template_names()

        return ['iam/login.token.html.j2']

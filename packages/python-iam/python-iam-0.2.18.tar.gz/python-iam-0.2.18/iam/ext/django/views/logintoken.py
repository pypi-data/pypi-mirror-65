"""Declares :class:`LoginTokenView`."""
import ioc
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView

import iam.lib.urls
from iam.domain import LoginCodeCredential
from .forms import BasePrincipalForm
from .subjectonboarding import SubjectOnboardingMixin


class LoginTokenView(SubjectOnboardingMixin, FormView):
    """Provides handlers for ``GET`` and ``POST`` requests to login using
    a temporary token.
    """
    template_name = 'iam/login.token.html.j2'

    class form_class(BasePrincipalForm):
        token = forms.CharField(required=True, max_length=6)
        otp = ioc.class_property('OneTimePasswordService')

        def clean(self):
            """Invoke the superclass :meth:`clean()` method and use the valid
            form data to check if the login code is valid.
            """
            data = super().clean()
            if not self.is_valid():
                return data
            self.subject = authenticate(
                realm=self.realm,
                principal=self.guess_principal(data['principal']),
                credential=LoginCodeCredential(data['token']))
            if not self.subject:
                self.add_error('token',
                    _('The code you entered is not valid.'))
            return data

    def get_initial(self):
        """Parse initial data from the query parameters."""
        initial = super().get_initial()
        if self.request.method == 'GET':
            initial = {x: self.request.GET[x]
                for x in dict.keys(self.request.GET)}
        return initial

    def form_valid(self, form):
        """The login token was valid and the user is authenticated."""
        subject = form.get_user()
        request = self.request
        if subject.haspassword():
            return super().form_valid(form)

        login(self.request, subject)
        redirect_to = iam.lib.urls.reverse('login')
        if request.META['QUERY_STRING']:
            redirect_to += '?'
            redirect_to += request.META['QUERY_STRING']
        return HttpResponseRedirect(redirect_to)

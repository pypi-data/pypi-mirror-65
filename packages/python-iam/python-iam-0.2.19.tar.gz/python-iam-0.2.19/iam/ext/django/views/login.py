"""Declares :class:`LoginView`."""
from django import forms
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import gettext_lazy as _

from .forms import ChoosePasswordForm
from .forms import PolymorphicPrincipalForm
from .subjectonboarding import SubjectOnboardingMixin


class LoginView(SubjectOnboardingMixin):
    """Exposes ``GET`` and ``POST`` methods to login a :term:`Subject`."""
    template_name = 'iam/login.html.j2'
    authentication_form = None
    form_class = PolymorphicPrincipalForm
    allow_signup = True

    class form_class(PolymorphicPrincipalForm):
        allow_create = False

    # TODO: Implement a mechanism to keep the below methods in sync.
    def must_redirect(self):
        """Return a boolean indicating if we must redirect an authenticated user
        away from this page.
        """
        subject = self.request.user
        redirect = super().must_redirect()
        if not subject.is_authenticated:
            return redirect

        # If the Subject has not accepted the terms of service, then it
        # should be prompted to do so. Same applies to the privacy policy. Staff
        # and superusers are exempt; these are assumed to have agreed to terms
        # of service/privacy policy prior to receiving their account credentials.
        if not subject.is_staff and not subject.is_superuser:
            if not subject.accepts(settings.IAM_TERMS_OF_SERVICE)\
            or not subject.accepts(settings.IAM_PRIVACY_POLICY):
                return False

        # Check if the user belongs to the realm specified by this
        # authentication gateway. If the user authenticated in a different,
        # log it out and provide an opportunity to login at this realm.
        if subject.realm_id != self.realm:
            logout(self.request)
            return False


        # If the user logged in with SSO then it should not be prompted to
        # set a password.
        if not subject.haspassword() and not self.request.sso:
            redirect = False

        # If the user has no first name or last name, prompt it to set it.
        if not subject.first_name or not subject.last_name:
            redirect = False

        return redirect

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update({
            self.redirect_field_name: self.get_redirect_url(),
            'site': current_site,
            'site_name': current_site.name,
            **(self.extra_context or {})
        })
        return context

    def get_form_class(self):
        """Return the appropriate form based on the ``op`` parameter in the
        POST-data.
        """
        form = super().get_form_class()
        if self.request.user.is_authenticated\
        and not self.request.user.haspassword()\
        and not self.request.sso:
            form = ChoosePasswordForm
            self.must_login = False

        return form

    def get_template_names(self):
        """Return a list of template names."""
        template_names = []
        if self.request.user.is_authenticated:
            subject = self.request.user
            if not subject.haspassword()\
            and not self.request.sso:
                # The user must choose a new password.
                template_names = ['iam/login.passwordexpired.html.j2']
            if not subject.accepts(settings.IAM_TERMS_OF_SERVICE):
                template_names = 'iam/login.useragreement.html.j2'
            elif not subject.accepts(settings.IAM_PRIVACY_POLICY):
                template_names = 'iam/login.useragreement.privacy.html.j2'
            elif not subject.first_name or not subject.last_name:
                template_names = ['iam/login.completenames.html.j2']
        else:
            template_names = super().get_template_names()
        return template_names

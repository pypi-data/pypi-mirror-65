"""Declares :class:`SubjectOnboardingMixin`."""
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import resolve_url
from django.utils.decorators import method_decorator
try:
    from django.utils.http import url_has_allowed_host_and_scheme
except ImportError:
    # Not available before Django 3.0
    url_has_allowed_host_and_scheme = lambda *a, **k: True
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView

from .iamcontextmixin import IAMContextMixin
from .successurlmixin import SuccessURLMixin


class SubjectOnboardingMixin(IAMContextMixin, SuccessURLMixin, FormView):
    """Mixin class that provides extra context to render login and registration
    pages.
    """
    must_login = True
    redirect_field_name = REDIRECT_FIELD_NAME
    redirect_authenticated_user = settings.IAM_REDIRECT_AUTHENTICATED_USER
    authentication_form = None

    @method_decorator(transaction.atomic)
    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if self.must_redirect():
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return FormView.dispatch(self, request, *args, **kwargs)

    def must_redirect(self):
        """Return a boolean indicating if we must redirect an authenticated user
        away from this page.
        """
        return self.redirect_authenticated_user\
            and self.request.user.is_authenticated

    def form_valid(self, form):
        """All security checks complete; log in the user."""
        if self.must_login:
            login(self.request, form.get_user())
        response = HttpResponseRedirect(self.get_success_url())

        # Set appropriate status code to prevent browsers from caching the
        # redirect URI, if any.
        response.status = 303
        return response

    def get_form_class(self):
        return self.authentication_form or self.form_class

    def get_form_kwargs(self):
        """Return the keyword arguments used to instantiate the form
        class.
        """
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['realm'] = self.get_realm()
        return kwargs

    def get_success_url(self):
        """Return the success URL to redirect when a valid form is
        submitted.
        """
        url = self.get_redirect_url()
        return url or resolve_url(settings.LOGIN_REDIRECT_URL)

    def get_redirect_url(self):
        """Return the user-originating redirect URL if it's safe."""
        redirect_to = self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, '')
        )
        url_is_safe = url_has_allowed_host_and_scheme(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )
        return redirect_to if url_is_safe else ''

    def get_template_names(self):
        """Return a list of template names. The default implementation simply
        returns :attr:`template_name`.
        """
        return [self.template_name]

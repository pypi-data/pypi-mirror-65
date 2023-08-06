"""Declares :class:`RedirectingFormView`."""
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import REDIRECT_FIELD_NAME
from django.contrib.auth.views import SuccessURLAllowedHostsMixin
from django.utils.decorators import method_decorator
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic import FormView
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters


DECORATORS = [never_cache, csrf_protect, sensitive_post_parameters,
    login_required]


@method_decorator(DECORATORS, 'dispatch')
class RedirectingFormView(SuccessURLAllowedHostsMixin, FormView):
    """A :class:`django.views.generic.FormView` implementation that
    redirects back to the URL provided in the query parameters.
    """
    redirect_field_name = REDIRECT_FIELD_NAME

    class base_form(forms.Form):

        def __init__(self, *args ,**kwargs):
            self.request = kwargs.pop('request', None)
            super().__init__(*args, **kwargs)

    def get_form_kwargs(self):
        """Return the keyword arguments used to instantiate the form
        class.
        """
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'request': self.request
        })
        return kwargs

    def get_success_url(self):
        """Return the user-originating redirect URL if it's safe. An
        unsafe URL indicates an attack probe.
        """
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

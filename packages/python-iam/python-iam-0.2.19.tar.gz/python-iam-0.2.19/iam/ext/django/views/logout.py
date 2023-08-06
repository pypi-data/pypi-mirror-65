"""Declares :class:`LogoutView`."""
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache

from .successurlmixin import SuccessURLMixin


class LogoutView(SuccessURLMixin, TemplateView):
    next_page = None
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'registration/logged_out.html'
    extra_context = None

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        next_page = self.get_next_page()
        if next_page:
            # Redirect to this page until the session has been cleared.
            return HttpResponseRedirect(next_page)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Logout may be done via POST."""
        return self.get(request, *args, **kwargs)

    def get_default_next_page(self):
        """Return the default next page if one isn't specified through the
        query parameter matching :attr:`redirect_field_name`.
        """
        return settings.LOGOUT_REDIRECT_URL

"""Declares view decorators."""
import functools
import urllib.parse

from django.conf import settings
from django.http import HttpResponseRedirect


def requireconsent(agreement, url=None):
    """Requires the :term:`Subject` to agree with the given agreement."""
    def decorator(func):
        @functools.wraps(func)
        def f(request, *args, **kwargs):
            redirect_to = url
            if url is None: # Nesting causes UnboundLocalError
                redirect_to = settings.LOGIN_URL
            redirect_to += '?'\
                    + urllib.parse.urlencode({'next': request.get_full_path()})
            if request.user.is_authenticated\
            and not request.user.accepts(agreement):
                return HttpResponseRedirect(redirect_to)
            return func(request, *args, **kwargs)
        return f
    return decorator

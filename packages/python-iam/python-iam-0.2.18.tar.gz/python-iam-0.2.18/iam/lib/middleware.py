"""Declares :class:`IAMMiddleware`."""
import ipaddress
import re

from django.contrib.auth import BACKEND_SESSION_KEY


class IAMMiddleware:
    """Sets various properties related to identity and access management
    on an incoming :term:`HTTP Request`.

    This request middleware requires session and must therefore appear after
    ``django.contrib.sessions.middleware.SessionMiddleware`` in the
    ``MIDDLEWARE`` setting.
    """

    #: Regular expression pattern that indicates if the backend used to
    #: authenticate was external (i.e. SSO).
    sso_backends_pattern = re.compile('^(social_core.backends|iam.lib.backends)\..*$')

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Set a flag indicating if the Subject authenticated through SSO.
        request.sso = False
        if request.session.get(BACKEND_SESSION_KEY):
            request.sso = bool(self.sso_backends_pattern.match(
                request.session[BACKEND_SESSION_KEY]))

        request.host = self.get_client_ip(request)

        return self.get_response(request)

    def get_client_ip(self, request):
        """Returns the remote address based on the ``HTTP_X_FORWARDED_FOR`` or
        ``REMOTE_ADDR`` headers.
        """
        remote_address = request.META.get('HTTP_CF_CONNECTING_IP')\
            or request.META.get('REMOTE_ADDR')
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            proxies = [str.strip(x) for x in str.split(x_forwarded_for, ',')]
            remote_address = proxies[-1]

        assert remote_address is not None
        return remote_address

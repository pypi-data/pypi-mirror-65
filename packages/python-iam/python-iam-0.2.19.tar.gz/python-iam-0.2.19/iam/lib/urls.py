"""URL helper functions."""
import urllib.parse

import django.urls
from django.conf import settings


def updateqs(url, params):
    """Update the query parameters in the URL and return a string containing
    the new URL.
    """
    parts = list(urllib.parse.urlparse(url))
    qs = dict(urllib.parse.parse_qsl(parts[4]))
    qs.update(params)
    parts[4] = urllib.parse.urlencode(qs)
    return urllib.parse.urlunparse(parts)


def reverse(name, *args, **kwargs):
    return django.urls.reverse(f'{settings.IAM_URL_NAMESPACE}:{name}', *args, **kwargs)


def reverse_lazy(name, *args, **kwargs):
    return django.urls.reverse_lazy(
        f'{settings.IAM_URL_NAMESPACE}:{name}', *args, **kwargs)

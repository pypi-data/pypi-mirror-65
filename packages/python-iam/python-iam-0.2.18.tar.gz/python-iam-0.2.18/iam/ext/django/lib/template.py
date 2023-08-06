import datetime
import re

import django.contrib.humanize.templatetags.humanize as humanize
import yaml
from django.contrib import messages
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from django.utils.translation import gettext, ngettext
from jinja2 import Environment


def naturaltime(value):
    if isinstance(value, int):
        if value == 0:
            value = 1
        value = datetime.datetime.fromtimestamp(value / 1000)
    return humanize.naturaltime(value)


def isactive(request, pattern):
    """Return a boolean indicating if a view with the given name
    is rendering the page.
    """
    return re.match(pattern, request.resolver_match.view_name)


def environment(**options):
    options.update({'extensions':['jinja2.ext.i18n']})
    env = Environment(**options)
    env.install_gettext_callables(gettext=gettext,
        ngettext=ngettext, newstyle=True)
    env.globals.update({
        'isactive': isactive,
        'static': staticfiles_storage.url,
        'url': reverse,
        'get_messages': messages.get_messages
    })
    env.filters.update({
        'naturaltime': naturaltime,
        'to_yaml': (lambda x: yaml.safe_dump(x, indent=2, default_flow_style=False)),
    })
    return env


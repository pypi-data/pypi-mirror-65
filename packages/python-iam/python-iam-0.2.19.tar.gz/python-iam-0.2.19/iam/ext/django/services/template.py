"""Declares :class:`TemplateService`."""
from unimatrix.ext.django import services


class TemplateService(services.TemplateService):
    """Provides an interface to render templates."""
    default_prefix = 'iam'

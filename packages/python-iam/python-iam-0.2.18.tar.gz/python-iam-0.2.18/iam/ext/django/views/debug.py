"""Declares :class:`DebugView`."""
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator

from .decorators import requireconsent
from .iamcontextmixin import IAMContextMixin



@method_decorator(requireconsent('terms'), 'dispatch')
@method_decorator(requireconsent('privacy'), 'dispatch')
class DebugView(IAMContextMixin, TemplateView):
    template_name = 'iam/debug.html.j2'
    splash_image = None

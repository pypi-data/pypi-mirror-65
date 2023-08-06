"""Declares :class:`BasePartialFormView`."""
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .iamcontextmixin import IAMContextMixin


@method_decorator(login_required, 'dispatch')
class BasePartialFormView(IAMContextMixin, FormView):
    """A :class:`django.forms.generic.FormView` implementation that renders
    only the form.
    """

    def form_invalid(self, *args, **kwargs):
        """Override the response code to return ``422``."""
        response = super().form_invalid(*args, **kwargs)
        response.status_code = 422
        return response

    def form_valid(self, form):
        """Return a HTTP response with the partial form."""
        return self.render_to_response(
            self.get_context_data(form=form))

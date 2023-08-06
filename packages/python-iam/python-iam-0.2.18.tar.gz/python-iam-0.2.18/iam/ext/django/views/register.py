"""Declares :class:`RegisterView`."""
from django import forms
from django.core.validators import MinLengthValidator

from ..lib.forms import NameField
from .forms import PolymorphicPrincipalForm
from .login import LoginView
from .subjectonboarding import SubjectOnboardingMixin


class RegisterView(LoginView):
    """Exposes ``GET`` and ``POST`` methods to register a new
    :term:`Subject`.
    """
    template_name = 'iam/register.html.j2'
    allow_signup = True

    class form_class(PolymorphicPrincipalForm):
        require_valid_credentials = False
        allow_create = True

        first_name = NameField(
            max_length=32,
            required=True,
        )

        last_name = NameField(
            max_length=32,
            required=True,
        )

        def create_subject(self, *args, **kwargs):
            """Creates a new :term:`Subject` that is identified by the given
            :term:`Principal` `principal` and :term:`Password` `password`. Return
            the :class:`~iam.ext.django.models.Subject` instance, or ``None``
            when the :term:`Principal` is already associated to a :term:`Subject`.
            """
            subject = super().create_subject(*args, **kwargs)
            if subject:
                subject.first_name = self.cleaned_data['first_name']
                subject.last_name = self.cleaned_data['last_name']
            return subject

    def form_valid(self, form):
        """All security checks complete; log in the user."""
        assert not self.request.user.is_authenticated,\
            "Subject should not be authenticated when using this form."
        subject = form.get_user()
        return super().form_valid(form)\
            if not subject.is_anonymous\
            else super().form_invalid(form)

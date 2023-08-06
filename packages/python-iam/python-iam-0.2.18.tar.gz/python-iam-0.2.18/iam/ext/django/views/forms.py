"""Declares :class:`PolymorphicPrincipalForm`."""
import ioc
from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _

from iam.domain import EmailPrincipal
from iam.domain import PhonenumberPrincipal
from iam.domain import NullPrincipal
from iam.domain import PasswordCredential
from iam.ext.django.models import Subject
from iam.ext.django.lib.forms import PrincipalField


class BasePrincipalForm(forms.Form):
    """Base class for all forms that need to guess principals."""

    #: A list of principal classes that are tried by the login form based
    #: in the `principal` input field. The first match is used.
    principal_classes = {
        'email': EmailPrincipal,
        'phonenumber': PhonenumberPrincipal,
    }

    principal = PrincipalField(
        max_length=128,
        required=True
    )

    def __init__(self, *args, **kwargs):
        self.realm = kwargs.pop('realm')
        self.request = kwargs.pop('request')
        self.subject = None
        super().__init__(*args, **kwargs)

    def clean_principal(self):
        """Resolves the provided principal to a concrete type."""
        if self.cleaned_data.get('principal'):
            self.guessed = self.guess_principal(self.cleaned_data['principal'])
            if type(self.guessed) == NullPrincipal:
                raise forms.ValidationError(f"Invalid input.", 'principal')
        return self.cleaned_data.get('principal')

    def get_principal_classes(self):
        """Returns the enabled principal classes."""
        return [self.principal_classes[x]
            for x in settings.IAM_ACCOUNT_PRINCIPALS] + [NullPrincipal]

    def get_principal(self, resolve=False):
        """Return a :class:`~iam.domain.Principal` instance using the value
        provided in the ``principal`` input field.
        """
        subject = None
        principal = self.guess_principal(self.cleaned_data['principal'])
        if resolve:
            try:
                self.subject = subject = principal.resolve(self.realm,
                    Subject.objects)
            except Subject.DoesNotExist:
                self.subject = subject = None
        return principal, subject

    def get_subject(self):
        """Return a :class:`~iam.ext.django.models.Subject` instance,
        identified by the :term:`Principal` from the input field.
        """
        if self.subject is not None:
            return self.subject
        _, self.subject = self.get_principal(resolve=True)
        return self.subject

    def get_subject_id(self):
        """Return the :term:`Subject Identifier`."""
        return self.get_subject().pk

    def get_user(self):
        """Returns the user found by the valid login credentials."""
        return self.subject

    def guess_principal(self, value):
        """Pattern matches a :term:`Principal Type` based on `value`."""
        for cls in self.get_principal_classes():
            if not cls.iscapable(value):
                continue
            break
        return cls(value)

class PolymorphicPrincipalForm(BasePrincipalForm):
    """Mixin class that determines the principal based on pattern
    matching, and retrieves the subject.
    """
    availability = ioc.class_property('PrincipalAvailabilityService')
    registration = ioc.class_property('RegistrationService')
    repo = ioc.class_property('SubjectRepository')

    #: Indicate that the form may create a new
    #: :class:`~iam.ext.django.models.Subject` based on the form parameters,
    #: if there was none prior existing.
    allow_create = False

    #: Indicate that the provided principal, password must authenticate
    #: to a :term:`Subject`. If :attr:`require_valid_credentials` is ``False``,
    #: then :meth:`get_user()` will return ``None`` instead of raising a
    #: :exc:`~django.forms.ValidationError` during form validation.
    require_valid_credentials = True

    password = forms.CharField(
        max_length=64,
        required=True,
        widget=forms.PasswordInput,
        validators=[
            MinLengthValidator(8)
        ]
    )

    def clean(self):
        """Looks up the subject specified by the input credential and
        raises a :exc:`ValidationError` if no subject could be
        authenticated. On success, add the
        :class:`~iam.ext.django.models.Subject` instance to the cleaned
        data.
        """
        assert not self.request.user.is_authenticated,\
            "Subject should not be authenticated when using this form."
        cleaned_data = super().clean()
        if not self.is_valid():
            return cleaned_data

        cleaned_data['realm'] = self.realm
        if cleaned_data.get('principal') and cleaned_data.get('password'):
            principal = self.guess_principal(cleaned_data['principal'])
            password = PasswordCredential(cleaned_data['password'])
            self.subject = authenticate(self.request, realm=self.realm,
                principal=principal, credential=password)
            if not self.subject:
                available = self.availability.isavailable(self.realm, principal)
                if self.require_valid_credentials and not available:
                    raise forms.ValidationError(
                        _("The login credentials that you provided are not "
                          "valid."))
                elif self.allow_create and available:
                    self.subject = self.create_subject(principal, password)
                elif not available:
                    # A Subject can be identified with the provided Principal,
                    # but its Credential was not valid.
                    self.fake_success = True
                else:
                    # The Principal is available, but we are not allowed
                    # to create Subjects.
                    raise forms.ValidationError(
                        _("The login credentials that you provided are not "
                          "valid."))

                # If no Subject was found at this point, we are an anonymous
                # user.
                if self.subject is None:
                    raise forms.ValidationError(
                        _("The login credentials that you provided are not "
                          "valid."))

            cleaned_data['subject'] = self.subject
            self.using = principal.kind

        return cleaned_data

    def create_subject(self, principal, password):
        """Creates a new :term:`Subject` that is identified by the given
        :term:`Principal` `principal` and :term:`Password` `password`. Return
        the :class:`~iam.ext.django.models.Subject` instance, or ``None``
        when the :term:`Principal` is already associated to a :term:`Subject`.
        """
        assert self.allow_create
        self.registration.register(self.request.host, self.request.site.domain,
            self.realm, principal, credentials=[password])
        return authenticate(self.request, realm=self.realm, principal=principal,
            credential=password)


class ChoosePasswordForm(forms.Form):
    password = ioc.class_property('PasswordService')

    password1 = forms.CharField(
        max_length=64,
        required=True,
        widget=forms.PasswordInput,
        validators=[
            MinLengthValidator(8)
        ]
    )
    password2 = forms.CharField(
        max_length=64,
        required=True,
        widget=forms.PasswordInput
    )

    def __init__(self, *args, **kwargs):
        self.realm = kwargs.pop('realm')
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean(self):
        """Invoke the superclass :meth:`clean()` method and ensure that
        the passwords are equal.
        """
        data = super().clean()
        if not self.is_valid():
            return data

        if data['password1'] != data['password2']:
            self.add_error('password2', _("The passwords do not match."))
            return data

        # TODO: This needs to be invoked in the controller
        self.password.change(self.request.user.pk, data['password1'])

        return data

    def get_password(self):
        """Return the password provided by the user."""
        return self.cleaned_data['password1']

    def get_user(self):
        """Return the :term:`Subject` for which the :term:`Password` is being
        chosen.
        """
        return self.request.user

"""Declares form fields and base classes."""
from django import forms
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext as _


def notallupper(value):
    """Ensure that `value` does not consist of only uppercase characters."""
    if str.upper(value) == value:
        raise forms.ValidationError(_("Do not use only uppercase characters."))


def notalllower(value):
    """Ensure that `value` does not consist of only lowercase characters."""
    if str.lower(value) == value:
        raise forms.ValidationError(_("Do not use only lowercase characters."))


def excludeforbidden(value):
    """Ensure that `value` does not contain forbidden characters."""
    forbidden = set([';','<','>'])
    if (set(value) & forbidden):
        raise forms.ValidationError("Stop probing.")


class NameField(forms.CharField):
    """A :class:`~django.forms.CharField` implementation that is used for
    first and last names.
    """

    def __init__(self, *args, **kwargs):
        validators = kwargs.setdefault('validators', [])
        validators.extend([
            MinLengthValidator(2),
            notallupper,
            notalllower,
            excludeforbidden
        ])
        super().__init__(*args, **kwargs)


class PrincipalField(forms.CharField):
    """A :class:`~django.forms.CharField` that ensures that a :term:`Principal`
    is always lowercase.
    """

    def clean(self, value):
        """Invokes :meth:`django.forms.Charfield.clean()` and lowercases the
        value.
        """
        return str.lower(super().clean(value))

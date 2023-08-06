#pylint: skip-file
import django.test
import unimatrix.lib.test
from django.contrib.auth import authenticate
from django.contrib.auth import login

from iam.const import TEST_USER1_PHONENUMBER
from iam.const import TEST_USER1_ID
from iam.const import TEST_PASSWORD
from iam.domain import PhonenumberPrincipal
from iam.domain import NullCredential
from iam.domain import PasswordCredential
from iam.ext.django.lib.backends import LocalSubjectBackend

from .test_login_email_and_password import PasswordAuthenticationTestCase


@unimatrix.lib.test.integration
class PasswordAuthenticationTestCase(PasswordAuthenticationTestCase):
    authenticate_kwargs = {
        'request': None,
        'principal': PhonenumberPrincipal(TEST_USER1_PHONENUMBER),
        'credential': PasswordCredential(TEST_PASSWORD)
    }

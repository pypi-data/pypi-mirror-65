#pylint: skip-file
import django.test
import unimatrix.lib.test
from django.contrib.auth import authenticate
from django.contrib.auth import login

from iam.const import TEST_USER1_EMAIL
from iam.const import TEST_USER1_ID
from iam.const import TEST_PASSWORD
from iam.domain import EmailPrincipal
from iam.domain import NullCredential
from iam.domain import PasswordCredential
from iam.ext.django.lib.backends import LocalSubjectBackend


@unimatrix.lib.test.integration
class PasswordAuthenticationTestCase(django.test.TestCase):
    fixtures = ['testusers']
    authenticate_kwargs = {
        'request': None,
        'principal': EmailPrincipal(TEST_USER1_EMAIL),
        'credential': PasswordCredential(TEST_PASSWORD)
    }

    def setUp(self):
        self.backend = LocalSubjectBackend()

    def get_authenticate_kwargs(self):
        return dict(self.authenticate_kwargs)

    def test_login_with_valid_credentials(self):
        sub = self.backend.authenticate(**self.get_authenticate_kwargs())
        self.assertIsNotNone(sub)
        self.assertEqual(str(sub.pk), TEST_USER1_ID)

    def test_login_with_invalid_credentials(self):
        params = self.get_authenticate_kwargs()
        params['credential'] = PasswordCredential('wrong password')
        sub = self.backend.authenticate(**params)
        self.assertIsNone(sub)

    def test_login_with_no_credentials(self):
        params = self.get_authenticate_kwargs()
        params['credential'] = PasswordCredential('')
        sub = self.backend.authenticate(**params)
        self.assertIsNone(sub)

    def test_login_with_none_credentials(self):
        params = self.get_authenticate_kwargs()
        params['credential'] = None
        sub = self.backend.authenticate(**params)
        self.assertIsNone(sub)

    def test_login_with_null_credentials(self):
        params = self.get_authenticate_kwargs()
        params['credential'] = NullCredential()
        sub = self.backend.authenticate(**params)
        self.assertIsNone(sub)

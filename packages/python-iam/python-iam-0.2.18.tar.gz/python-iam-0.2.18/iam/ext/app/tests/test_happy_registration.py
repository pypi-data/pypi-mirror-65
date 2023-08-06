#pylint: skip-file
import django.test
import unimatrix.lib.test
from django.conf import settings

import iam.const
from iam.ext.django.models import Subject


@unimatrix.lib.test.integration
class RegistrationHappyFlowTestCase(django.test.TestCase):
    fixtures = ['testusers']

    def setUp(self):
        self.client = django.test.Client(HTTP_HOST='example.com')

    def test_register_with_email(self):
        response = self.client.post('/nl/registreren', {
            'principal': "happy.flow@test.unimatrixone.io",
            'password': 'foobarbaz',
            'first_name': 'Happy',
            'last_name': 'Flow'
        })

        # On succesful registration, the system must issue a redirect to
        # the default post-login page.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], settings.LOGIN_REDIRECT_URL)

        # If the current request is authenticated, the login page must redirect
        # to the default postlogin page.
        response = self.client.get('/nl/aanmelden/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], settings.LOGIN_REDIRECT_URL)

        return response

    def test_can_login_after_registration(self):
        response = self.client.post('/nl/registreren', {
            'principal': "happy.flow@test.unimatrixone.io",
            'password': 'foobarbaz',
            'first_name': 'Happy',
            'last_name': 'Flow'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], settings.LOGIN_REDIRECT_URL)

        # Instantiate a new, unauthenticated client.
        client = django.test.Client(HTTP_HOST='example.com')
        response = client.get('/nl/aanmelden/')
        self.assertEqual(response.status_code, 200)

        response = client.post('/nl/aanmelden/', {
            'principal': "happy.flow@test.unimatrixone.io",
            'password': 'foobarbaz',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], settings.LOGIN_REDIRECT_URL)

    def test_register_with_email_and_next_parameter(self):
        response = self.client.post('/nl/registreren?next=/foo', {
            'principal': "happy.flow@test.unimatrixone.io",
            'password': 'foobarbaz',
            'first_name': 'Happy',
            'last_name': 'Flow'
        })

        # On succesful registration, the system must issue a redirect to
        # the default post-login page and redirect to the parameter provided
        # by ?next.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/foo')

        # If the current request is authenticated, the login page must redirect
        # to the parameter specified by ?next.
        response = self.client.get('/nl/aanmelden/?next=/foo')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/foo')

    def test_register_with_email_for_existing_user_redirects_to_default(self):
        # When a registration attempt is made with an email address that is
        # associated to an existing account, and the password matches, then
        # the application must redirect to the default login page.
        response = self.client.post('/nl/registreren', {
            'principal': iam.const.TEST_USER1_EMAIL,
            'password': iam.const.TEST_PASSWORD,
            'first_name': 'Happy',
            'last_name': 'Flow'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], settings.LOGIN_REDIRECT_URL)

    def test_register_with_email_for_existing_user_redirects_to_next(self):
        # When a registration attempt is made with an email address that is
        # associated to an existing account, and the password matches, then
        # the application must redirect to parameter specified by ?next.
        response = self.client.post('/nl/registreren?next=/foo', {
            'principal': iam.const.TEST_USER1_EMAIL,
            'password': iam.const.TEST_PASSWORD,
            'first_name': 'Happy',
            'last_name': 'Flow'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/foo')

    def test_register_with_email_for_existing_user_with_invalid(self):
        # When a registration attempt is made with an email address that is
        # associated to an existing account, and the password do not match,
        # then the application must not authenticate the user and display
        # a message that a confirmation email/sms is sent.
        response = self.client.post('/nl/registreren', {
            'principal': iam.const.TEST_USER1_EMAIL,
            'password': iam.const.TEST_PASSWORD + 'a',
            'first_name': 'Happy',
            'last_name': 'Flow'
        })
        self.assertEqual(response.status_code, 200)

    def test_register_does_not_create_subject_on_invalid_first_name(self):
        # When a registration attempt is made with an invalid form submission,
        # then a Subject instance must not be created.
        response = self.client.post('/nl/registreren', {
            'principal': "happy.flow@test.unimatrixone.io",
            'password': 'foobarbaz',
            'first_name': 'H',
            'last_name': 'Flow'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(not Subject.objects.filter(
            principals__value='happy.flow@test.unimatrixone.io').exists())

    def test_register_does_not_create_subject_on_invalid_last_name(self):
        # When a registration attempt is made with an invalid form submission,
        # then a Subject instance must not be created.
        response = self.client.post('/nl/registreren', {
            'principal': "happy.flow@test.unimatrixone.io",
            'password': 'foobarbaz',
            'first_name': 'Happy',
            'last_name': 'F'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(not Subject.objects.filter(
            principals__value='happy.flow@test.unimatrixone.io').exists())

    def test_register_does_not_create_subject_on_invalid_principal(self):
        # When a registration attempt is made with an invalid form submission,
        # then a Subject instance must not be created.
        response = self.client.post('/nl/registreren', {
            'principal': "123",
            'password': 'foobarbaz',
            'first_name': 'Happy',
            'last_name': 'F'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(not Subject.objects.filter(
            principals__value='123').exists())

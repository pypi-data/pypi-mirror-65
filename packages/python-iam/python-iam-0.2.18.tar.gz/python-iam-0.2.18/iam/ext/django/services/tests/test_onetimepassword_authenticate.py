#pylint: skip-file
import unimatrix.lib.test
import django.test

from iam.const import TEST_USER1_ID
from ...models import LoginCode
from ..onetimepassword import OneTimePasswordService


@unimatrix.lib.test.integration
class OneTimePasswordAuthenticationTestCase(django.test.TestCase):
    fixtures = ['testusers']
    subject = TEST_USER1_ID

    def setUp(self):
        # Ensure that the minimum lifetime is not enforced.
        self.lifetime = LoginCode.MIN_LIFETIME
        LoginCode.MIN_LIFETIME = 0
        self.service = OneTimePasswordService()
        self.service.generate(self.subject)

    def tearDown(self):
        LoginCode.MIN_LIFETIME = self.lifetime

    def test_valid_code_can_authenticate(self):
        dao = LoginCode.objects.get(subject=self.subject)
        self.assertTrue(self.service.verify(self.subject, dao.code))

    def test_invalid_code_can_not_authenticate(self):
        self.assertFalse(self.service.verify(self.subject, '0'))

    def test_code_get_deleted_after_max_attempts(self):
        # The database entity must be deleted after MAX_ATTEMPTS
        # is reached, to prevent against enumeration attacks and guesses.
        self.assertTrue(LoginCode.objects.filter(subject=self.subject).exists())
        for i in range(LoginCode.MAX_ATTEMPTS + 1):
            self.assertFalse(self.service.verify(self.subject, '0'))
        self.assertFalse(LoginCode.objects.filter(subject=self.subject).exists())

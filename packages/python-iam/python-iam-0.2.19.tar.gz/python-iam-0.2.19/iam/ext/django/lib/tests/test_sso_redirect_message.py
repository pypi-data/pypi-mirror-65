#pylint: skip-file
import unittest

import unimatrix.lib.test
from django.conf import settings
from django.test import RequestFactory

from iam.const import MESSAGE_QUERY_PARAM
from ..auth import on_redirected


@unimatrix.lib.test.unit
class RedirectMessageVerificationTestCase(unittest.TestCase):
    """Tests if a message is correctly verified on SSO redirect."""

    def setUp(self):
        self.factory = RequestFactory()

    def test_no_message_is_ignored(self):
        request = self.factory.get('/')
        self.assertIsNone(on_redirected(request))

    def test_invalid_message_interrupts_pipeline(self):
        request = self.factory.get('/', {MESSAGE_QUERY_PARAM: 'ffoo'})

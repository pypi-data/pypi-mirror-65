#pylint: skip-file
import unittest

import unimatrix.lib.test

from ..emailprincipal import EmailPrincipal


@unimatrix.lib.test.unit
class EmailPrincipalDetectionTestCase(unittest.TestCase):
    """Tests that email addresses are detected by the ``iscapable()``
    method.
    """
    values = [
        'foo@bar.baz'
    ]
    cls = EmailPrincipal


    def test_iscapable(self):
        for value in self.values:
            self.assertTrue(self.cls.iscapable(value))

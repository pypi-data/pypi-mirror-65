#pylint: skip-file
import unittest

import unimatrix.lib.test

from ..phonenumberprincipal import PhonenumberPrincipal


@unimatrix.lib.test.unit
class PhonenumberPrincipalDetectionTestCase(unittest.TestCase):
    """Tests that email addresses are detected by the ``iscapable()``
    method.
    """
    values = [
        '+31612345678'
    ]
    cls = PhonenumberPrincipal


    def test_iscapable(self):
        for value in self.values:
            self.assertTrue(self.cls.iscapable(value))

__author__ = 'kohn'

import unittest
from mendeleycache.utils import validator


class TestMendeleyValidators(unittest.TestCase):

    def test_is_valid_mendeley_id(self):
        self.assertTrue(validator.is_valid_mendeley_id('d0b7f41f-ad37-3b47-ab70-9feac35557cc'))
        self.assertFalse(validator.is_valid_mendeley_id('d0b7f41f)-ad37-3b47-ab70-9feac35557cc'))

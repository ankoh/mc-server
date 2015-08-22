__author__ = 'kohn'

from mendeleycache.analyzer.validator import is_field_tag
import unittest


class TestValidator(unittest.TestCase):

    def test_is_field_tag(self):
        self.assertTrue(is_field_tag("cyber-physical-systems"))
__author__ = 'kohn'

from mendeleycache.utils.files import get_relative_path
from mendeleycache.mendeleycache import MendeleyCache

from os import remove
from os.path import exists

import unittest


class TestApp(unittest.TestCase):
    def test_app_startup(self):
        app = MendeleyCache('mendeleycache')
        app.debug = True
        sut = app.test_client()

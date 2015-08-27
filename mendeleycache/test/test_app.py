__author__ = 'kohn'

from mendeleycache.utils.files import get_relative_path
from mendeleycache.mendeleycache import MendeleyCache

from os import remove
from os.path import exists

import unittest


class TestApp(unittest.TestCase):
    config_path = get_relative_path('config.yml')

    @staticmethod
    def write_debug_config():
        # Write valid configuration file
        with open(TestApp.config_path, 'w') as config:
            config.truncate()
            valid_config = (
                "mendeley:\n"
                "  app_id: 231209\n"
                "  app_secret: AlPhA4NuMeRiC20\n"
                "  research_group: d0b7f41f-ad37-3b47-ab70-9feac35557cc\n"
                "\n"
                "database:\n"
                "  engine: sqlite\n"
                "  path: ''\n"
            )
            config.write(valid_config)

    def test_app_startup(self):
        TestApp.write_debug_config()
        app = MendeleyCache('mendeleycache')
        app.debug = True
        sut = app.test_client()

    def tearDown(self):
        remove(TestApp.config_path) if exists(TestApp.config_path) else None
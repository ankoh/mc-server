__author__ = 'kohn'

from os import remove
from os.path import exists
from mendeleycache.utils.files import get_path
from mendeleycache.utils.exceptions import InvalidConfigurationException
from mendeleycache.config import ServiceConfiguration

import unittest


class TestServiceConfiguration(unittest.TestCase):
    config_file = get_path('config.yml')

    def write_valid(self):
        with open(self.config_file, 'w') as config:
            config.truncate()
            valid_config = (
                "mendeley:\n"
                "  app_id: 231209\n"
                "  app_secret: AlPhA4NuMeRiC20\n"
                "  research_group: d0b7f41f-ad37-3b47-ab70-9feac35557cc\n"
                "\n"
                "database:\n"
                "  hostname: localhost\n"
                "  port: 12413\n"
                "  db: mendeleycache\n"
                "  user: root\n"
                "  secret: 42\n"
            )
            config.write(valid_config)

    def write_invalid_1(self):
        with open(self.config_file, 'w') as config:
            config.truncate()
            invalid_config = (
                "blabla:\n"
                "  app_id: 231209\n"
                "  app_secret: AlPhA4NuMeRiC20\n"
                "  research_group: d0b7f41f-ad37-3b47-ab70-9feac35557cc\n"
                "\n"
                "database:\n"
                "  hostname: localhost\n"
                "  port: 12413\n"
                "  db: mendeleycache\n"
                "  user: root\n"
                "  secret: 42\n"
            )
            config.write(invalid_config)

    def test_service_configuration_load(self):
        # test a non existent configuration
        config = ServiceConfiguration()
        remove(self.config_file) if exists(self.config_file) else None
        self.assertRaises(InvalidConfigurationException, config.load)

        # then test an invalid configuration
        config = ServiceConfiguration()
        self.write_invalid_1()
        self.assertRaises(InvalidConfigurationException, config.load)

        # then test a valid configuration
        config = ServiceConfiguration()
        self.write_valid()
        try:
            config.load()
            self.assertEqual(config.mendeley.app_id, 231209)
            self.assertEqual(config.mendeley.app_secret, "AlPhA4NuMeRiC20")
            self.assertEqual(config.mendeley.research_group, "d0b7f41f-ad37-3b47-ab70-9feac35557cc")
            self.assertEqual(config.database.hostname, "localhost")
            self.assertEqual(config.database.port, 12413)
            self.assertEqual(config.database.db, "mendeleycache")
            self.assertEqual(config.database.user, "root")
            self.assertEqual(config.database.secret, 42)
        except InvalidConfigurationException as e:
            self.fail(e)


    def tearDown(self):
        remove(self.config_file) if exists(self.config_file) else None
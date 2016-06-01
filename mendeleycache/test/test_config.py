__author__ = 'kohn'

from os import remove
from os.path import exists
import os
from mendeleycache.utils.files import get_relative_path
from mendeleycache.utils.exceptions import InvalidConfigurationException
from mendeleycache.config import ServiceConfiguration

import unittest


class TestServiceConfiguration(unittest.TestCase):
    @staticmethod
    def delete_environment():
        if "MC_CRAWLER" in os.environ:
            del os.environ["MC_CRAWLER"]
        if "MC_APP_ID" in os.environ:
            del os.environ["MC_APP_ID"]
        if "MC_APP_SECRET" in os.environ:
            del os.environ["MC_APP_SECRET"]
        if "MC_RESEARCH_GROUP" in os.environ:
            del os.environ["MC_RESEARCH_GROUP"]
        if "MC_DATABASE_PATH" in os.environ:
            del os.environ["MC_DATABASE_PATH"]
        if "MC_PROFILE_PAGE_PATTERN" in os.environ:
            del os.environ["MC_PROFILE_PAGE_PATTERN"]

    @staticmethod
    def write_valid_1():
        TestServiceConfiguration.delete_environment()
        os.environ["MC_CRAWLER"] = "mendeley"
        os.environ["MC_APP_ID"] = "231209"
        os.environ["MC_APP_SECRET"] = "AlPhA4NuMeRiC20"
        os.environ["MC_RESEARCH_GROUP"] = "d0b7f41f-ad37-3b47-ab70-9feac35557cc"
        os.environ["MC_PROFILE_PAGE_PATTERN"] = "www1.in.tum.de/:firstname-:lastname"

    @staticmethod
    def write_valid_2():
        TestServiceConfiguration.delete_environment()
        os.environ["MC_CRAWLER"] = "mendeley"
        os.environ["MC_APP_ID"] = "231209"
        os.environ["MC_APP_SECRET"] = "AlPhA4NuMeRiC20"
        os.environ["MC_RESEARCH_GROUP"] = "d0b7f41f-ad37-3b47-ab70-9feac35557cc"

        os.environ["MC_DATABASE_ENGINE"] = "sqlite"
        os.environ["MC_DATABASE_PATH"] = ""

    def test_service_configuration_load(self):
        # then test a valid mysql configuration
        config = ServiceConfiguration()
        TestServiceConfiguration.write_valid_1()
        try:
            config.load()
            self.assertEqual(config.crawler.app_id, "231209")
            self.assertEqual(config.crawler.app_secret, "AlPhA4NuMeRiC20")
            self.assertEqual(config.crawler.research_group, "d0b7f41f-ad37-3b47-ab70-9feac35557cc")
            self.assertEqual(config.cache.profile_page_pattern, "www1.in.tum.de/:firstname-:lastname")
        except InvalidConfigurationException as e:
            self.fail(e)

        # then test a valid sqlite configuration
        config = ServiceConfiguration()
        TestServiceConfiguration.write_valid_2()
        try:
            config.load()
            self.assertEqual(config.crawler.app_id, "231209")
            self.assertEqual(config.crawler.app_secret, "AlPhA4NuMeRiC20")
            self.assertEqual(config.crawler.research_group, "d0b7f41f-ad37-3b47-ab70-9feac35557cc")
            self.assertEqual(config.database.engine, "sqlite")
            self.assertEqual(config.database.path, "")
            self.assertEqual(config.cache.profile_page_pattern, "")
        except InvalidConfigurationException as e:
            self.fail(e)

    def tearDown(self):
        TestServiceConfiguration.delete_environment()

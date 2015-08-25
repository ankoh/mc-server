__author__ = 'kohn'

import unittest

from mendeleycache.config import SQLiteConfiguration
from mendeleycache.data.controller import DataController
from mendeleycache.data.api_scripts import ApiScripts


class TestCrawlScripts(unittest.TestCase):

    def test_replace_mendeley_documents(self):
        sqlite_in_memory = SQLiteConfiguration("sqlite", "")
        data_controller = DataController(sqlite_in_memory)
        data_controller.run_schema()

        # The call shall not crash with empty input
        r = data_controller.crawl_data.replace_mendeley_documents([])
        self.assertIsNone(r)

    def test_replace_mendeley_profiles(self):
        sqlite_in_memory = SQLiteConfiguration("sqlite", "")
        data_controller = DataController(sqlite_in_memory)
        data_controller.run_schema()

        # The call shall not crash with empty input
        r = data_controller.crawl_data.replace_mendeley_profiles([])
        self.assertIsNone(r)

    def test_update_cache_documents(self):
        sqlite_in_memory = SQLiteConfiguration("sqlite", "")
        data_controller = DataController(sqlite_in_memory)
        data_controller.run_schema()

        # The call shall not crash with empty input
        r = data_controller.crawl_data.update_cache_documents(dict())
        self.assertIsNone(r)

    def test_update_cache_profiles(self):
        sqlite_in_memory = SQLiteConfiguration("sqlite", "")
        data_controller = DataController(sqlite_in_memory)
        data_controller.run_schema()

        # The call shall not crash with empty input
        r = data_controller.crawl_data.update_cache_profiles(dict())
        self.assertIsNone(r)

    def test_update_cache_fields(self):
        sqlite_in_memory = SQLiteConfiguration("sqlite", "")
        data_controller = DataController(sqlite_in_memory)
        data_controller.run_schema()

        # The call shall not crash with empty input
        r = data_controller.crawl_data.update_cache_fields(dict())
        self.assertIsNone(r)

    def test_link_profiles_to_documents(self):
        sqlite_in_memory = SQLiteConfiguration("sqlite", "")
        data_controller = DataController(sqlite_in_memory)
        data_controller.run_schema()

        # The call shall not crash with empty input
        r = data_controller.crawl_data.link_profiles_to_documents(dict(), dict())
        self.assertIsNone(r)

    def test_link_fields_to_documents(self):
        sqlite_in_memory = SQLiteConfiguration("sqlite", "")
        data_controller = DataController(sqlite_in_memory)
        data_controller.run_schema()

        # The call shall not crash with empty input
        r = data_controller.crawl_data.link_fields_to_documents(dict())
        self.assertIsNone(r)

__author__ = 'kohn'

import unittest

from mendeleycache.config import SQLiteConfiguration
from mendeleycache.data.controller import DataController
from mendeleycache.data.api_scripts import ApiScripts

from mendeleycache.models import Profile

class TestCrawlScripts(unittest.TestCase):

    def test_replace_documents(self):
        sqlite_in_memory = SQLiteConfiguration("sqlite", "")
        data_controller = DataController(sqlite_in_memory)
        data_controller.run_schema()

        # The call shall not crash with empty input
        r = data_controller.crawl_data.replace_documents([])
        self.assertIsNone(r)

    def test_replace_profiles(self):
        sqlite_in_memory = SQLiteConfiguration("sqlite", "")
        data_controller = DataController(sqlite_in_memory)
        data_controller.run_schema()

        # The call shall not crash with empty input
        r = data_controller.crawl_data.replace_profiles([])
        self.assertIsNone(r)

        profile1 = Profile("id1", "Hans", "Mustermann", "", "")
        profile2 = Profile("id2", "Max", "Mustermann", "", "")
        data_controller.crawl_data.replace_profiles([profile1, profile2])

        # Check data count in the table
        cnt = data_controller.engine.execute("SELECT COUNT(*) FROM profile").fetchone()
        self.assertEqual(cnt[0], 2)

        # Then query rows
        rows = data_controller.engine.execute(
            "SELECT mid, unified_name, first_name, last_name, display_name "
            "FROM profile "
        ).fetchall()

        # Check first row
        self.assertEqual(rows[0]["mid"], "id1")
        self.assertEqual(rows[0]["unified_name"], "hansmustermann")
        self.assertEqual(rows[0]['first_name'], "Hans")
        self.assertEqual(rows[0]['last_name'], "Mustermann")

        # Check second row
        self.assertEqual(rows[1]["mid"], "id2")
        self.assertEqual(rows[1]["unified_name"], "maxmustermann")
        self.assertEqual(rows[1]['first_name'], "Max")
        self.assertEqual(rows[1]['last_name'], "Mustermann")

        profile1 = Profile("id1", "Hans", "Supermann", "", "")
        profile2 = Profile("id2", "Max", "Mustermann", "", "")
        data_controller.crawl_data.replace_profiles([profile1, profile2])

        # Check data count in the table
        cnt = data_controller.engine.execute("SELECT COUNT(*) FROM profile").fetchone()
        self.assertEqual(cnt[0], 2)

        # Then query rows
        rows = data_controller.engine.execute(
            "SELECT mid, unified_name, first_name, last_name, display_name "
            "FROM profile "
        ).fetchall()

        # Check first row
        self.assertEqual(rows[0]["mid"], "id1")
        self.assertEqual(rows[0]["unified_name"], "hanssupermann")
        self.assertEqual(rows[0]['first_name'], "Hans")
        self.assertEqual(rows[0]['last_name'], "Supermann")


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

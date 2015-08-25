__author__ = 'kohn'

import unittest

from mendeleycache.config import SQLiteConfiguration
from mendeleycache.data.controller import DataController
from mendeleycache.data.api_scripts import ApiScripts

from mendeleycache.models import Profile, Document
from datetime import datetime


class TestCrawlScripts(unittest.TestCase):

    def test_replace_documents(self):
        sqlite_in_memory = SQLiteConfiguration("sqlite", "")
        data_controller = DataController(sqlite_in_memory)
        data_controller.run_schema()

        # The call shall not crash with empty input
        r = data_controller.crawl_data.replace_documents([])
        self.assertIsNone(r)

        document1 = Document(
            core_id="doc1",
            core_profile_id="id1",
            core_title="title1",
            core_type="conference_proceedings",
            core_created=datetime.now(),
            core_last_modified=datetime.now(),
            core_abstract="blabla",
            core_source="ACM xy",
            core_year=2015,
            core_authors=[("Hans", "Mustermann"), ("Nicht", "Existent")],
            core_keywords=[],
            tags=["t ag- 1"]
        )
        document2 = Document(
            core_id="doc2",
            core_profile_id="id2",
            core_title="title2",
            core_type="conference_proceedings",
            core_created=datetime.now(),
            core_last_modified=datetime.now(),
            core_abstract="blabla2",
            core_source="ACM xyz",
            core_year=2014,
            core_authors=[],
            core_keywords=[],
            tags=[]
        )
        data_controller.crawl_data.replace_documents([document1, document2])

        # Check data count in the table
        cnt = data_controller.engine.execute("SELECT COUNT(*) FROM document").fetchone()
        self.assertEqual(cnt[0], 2)

        # Then query rows
        rows = data_controller.engine.execute(
            "SELECT mid, unified_title, title, owner_mid, doc_type, "
            " created, last_modified, abstract, source, pub_year "
            "FROM document "
        ).fetchall()

        # Check first row
        self.assertEqual(rows[0]["mid"], "doc1")
        self.assertEqual(rows[0]["unified_title"], "title1")
        self.assertEqual(rows[0]['title'], "title1")
        self.assertEqual(rows[0]['owner_mid'], "id1")
        self.assertEqual(rows[0]["doc_type"], "conference_proceedings")
        self.assertEqual(rows[0]['abstract'], "blabla")
        self.assertEqual(rows[0]["source"], "ACM xy")
        self.assertEqual(rows[0]["pub_year"], 2015)

        # Check second row
        self.assertEqual(rows[1]["mid"], "doc2")
        self.assertEqual(rows[1]["unified_title"], "title2")
        self.assertEqual(rows[1]['title'], "title2")
        self.assertEqual(rows[1]['owner_mid'], "id2")
        self.assertEqual(rows[1]["doc_type"], "conference_proceedings")
        self.assertEqual(rows[1]['abstract'], "blabla2")
        self.assertEqual(rows[1]["source"], "ACM xyz")
        self.assertEqual(rows[1]["pub_year"], 2014)

        document1 = Document(
            core_id="doc1",
            core_profile_id="id1",
            core_title="newtitle1",
            core_type="conference_proceedings",
            core_created=datetime.now(),
            core_last_modified=datetime.now(),
            core_abstract="blablaNew",
            core_source="ACM xyz1",
            core_year=2015,
            core_authors=[],
            core_keywords=[],
            tags=[]
        )
        document2 = Document(
            core_id="doc2",
            core_profile_id="id2",
            core_title="title2",
            core_type="conference_proceedings",
            core_created=datetime.now(),
            core_last_modified=datetime.now(),
            core_abstract="blabla2",
            core_source="ACM xyz",
            core_year=2014,
            core_authors=[],
            core_keywords=[],
            tags=[]
        )

        data_controller.crawl_data.replace_documents([document1, document2])

        # Check data count in the table
        cnt = data_controller.engine.execute("SELECT COUNT(*) FROM document").fetchone()
        self.assertEqual(cnt[0], 2)

        # Then query rows
        rows = data_controller.engine.execute(
            "SELECT mid, unified_title, title, owner_mid, doc_type, "
            " created, last_modified, abstract, source, pub_year "
            "FROM document "
        ).fetchall()

         # Check first row
        self.assertEqual(rows[0]["mid"], "doc1")
        self.assertEqual(rows[0]["unified_title"], "newtitle1")
        self.assertEqual(rows[0]['title'], "newtitle1")
        self.assertEqual(rows[0]['owner_mid'], "id1")
        self.assertEqual(rows[0]["doc_type"], "conference_proceedings")
        self.assertEqual(rows[0]['abstract'], "blablaNew")
        self.assertEqual(rows[0]["source"], "ACM xyz1")
        self.assertEqual(rows[0]["pub_year"], 2015)

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

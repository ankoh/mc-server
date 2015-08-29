__author__ = 'kohn'

import unittest

from mendeleycache.config import SQLiteConfiguration
from mendeleycache.data.controller import DataController
from mendeleycache.data.api_data import ApiData
from mendeleycache.data.identifiers import generate_id

from mendeleycache.models import Profile, Document, CacheField
from datetime import datetime


class TestCrawlScripts(unittest.TestCase):

    def test_update_documents(self):
        sqlite_in_memory = SQLiteConfiguration("")
        data_controller = DataController(sqlite_in_memory)
        data_controller.run_schema()

        # The call shall not crash with empty input
        r = data_controller.crawl_data.update_documents([])
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
        data_controller.crawl_data.update_documents([document1, document2])

        # Check data count in the table
        cnt = data_controller.engine.execute("SELECT COUNT(*) FROM document").fetchone()
        self.assertEqual(cnt[0], 2)

        # Then query rows
        rows = data_controller.engine.execute(
            "SELECT id, mendeley_id, cache_document_id, owner_mendeley_id,"
            " title, doc_type, created, last_modified, abstract, source, pub_year "
            "FROM document "
        ).fetchall()

        # Check first row
        self.assertEqual(rows[0]["mendeley_id"], "doc1")
        self.assertEqual(rows[0]["cache_document_id"], generate_id("title1"))
        self.assertEqual(rows[0]["owner_mendeley_id"], "id1")
        self.assertEqual(rows[0]['title'], "title1")
        self.assertEqual(rows[0]["doc_type"], "conference_proceedings")
        self.assertEqual(rows[0]['abstract'], "blabla")
        self.assertEqual(rows[0]["source"], "ACM xy")
        self.assertEqual(rows[0]["pub_year"], 2015)

        # Check second row
        self.assertEqual(rows[1]["mendeley_id"], "doc2")
        self.assertEqual(rows[1]["cache_document_id"], generate_id("title2"))
        self.assertEqual(rows[1]["owner_mendeley_id"], "id2")
        self.assertEqual(rows[1]['title'], "title2")
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

        data_controller.crawl_data.update_documents([document1, document2])

        # Check data count in the table
        cnt = data_controller.engine.execute("SELECT COUNT(*) FROM document").fetchone()
        self.assertEqual(cnt[0], 2)

        # Then query rows
        rows = data_controller.engine.execute(
            "SELECT id, mendeley_id, cache_document_id, owner_mendeley_id,"
            " title, doc_type, created, last_modified, abstract, source, pub_year "
            "FROM document "
        ).fetchall()

         # Check first row
        self.assertEqual(rows[0]["mendeley_id"], "doc1")
        self.assertEqual(rows[0]["cache_document_id"], generate_id("newtitle1"))
        self.assertEqual(rows[0]["owner_mendeley_id"], "id1")
        self.assertEqual(rows[0]['title'], "newtitle1")
        self.assertEqual(rows[0]["doc_type"], "conference_proceedings")
        self.assertEqual(rows[0]['abstract'], "blablaNew")
        self.assertEqual(rows[0]["source"], "ACM xyz1")
        self.assertEqual(rows[0]["pub_year"], 2015)

    def test_update_profiles(self):
        sqlite_in_memory = SQLiteConfiguration("")
        data_controller = DataController(sqlite_in_memory)
        data_controller.run_schema()

        # The call shall not crash with empty input
        r = data_controller.crawl_data.update_profiles([])
        self.assertIsNone(r)

        profile1 = Profile("id1", "Hans", "Mustermann", "", "")
        profile2 = Profile("id2", "Max", "Mustermann", "", "")
        data_controller.crawl_data.update_profiles([profile1, profile2])

        # Check data count in the table
        cnt = data_controller.engine.execute("SELECT COUNT(*) FROM profile").fetchone()
        self.assertEqual(cnt[0], 2)

        # Then query rows
        rows = data_controller.engine.execute(
            "SELECT id, mendeley_id, cache_profile_id, first_name, last_name, display_name "
            "FROM profile "
        ).fetchall()

        # Check first row
        self.assertEqual(rows[0]["mendeley_id"], "id1")
        self.assertEqual(rows[0]["cache_profile_id"], generate_id("hansmustermann"))
        self.assertEqual(rows[0]['first_name'], "Hans")
        self.assertEqual(rows[0]['last_name'], "Mustermann")

        # Check second row
        self.assertEqual(rows[1]["mendeley_id"], "id2")
        self.assertEqual(rows[1]["cache_profile_id"], generate_id("maxmustermann"))
        self.assertEqual(rows[1]['first_name'], "Max")
        self.assertEqual(rows[1]['last_name'], "Mustermann")

        profile1 = Profile("id1", "Hans", "Supermann", "", "")
        profile2 = Profile("id2", "Max", "Mustermann", "", "")
        data_controller.crawl_data.update_profiles([profile1, profile2])

        # Check data count in the table
        cnt = data_controller.engine.execute("SELECT COUNT(*) FROM profile").fetchone()
        self.assertEqual(cnt[0], 2)

        # Then query rows
        rows = data_controller.engine.execute(
            "SELECT id, mendeley_id, cache_profile_id, first_name, last_name, display_name "
            "FROM profile "
        ).fetchall()

        # Check first row
        self.assertEqual(rows[0]["mendeley_id"], "id1")
        self.assertEqual(rows[0]["cache_profile_id"], generate_id("hanssupermann"))
        self.assertEqual(rows[0]['first_name'], "Hans")
        self.assertEqual(rows[0]['last_name'], "Supermann")

    def test_update_cache_documents(self):
        sqlite_in_memory = SQLiteConfiguration("")
        data_controller = DataController(sqlite_in_memory)
        data_controller.run_schema()

        # The call shall not crash with empty input
        r = data_controller.crawl_data.update_cache_documents(dict())
        self.assertIsNone(r)

        document1 = Document(
            core_id="doc1",
            core_profile_id="id1",
            core_title="sametitle1",
            core_type="conference_proceedings",
            core_created=datetime.now(),
            core_last_modified=datetime.now(),
            core_abstract="Older Abtract",
            core_source="Older source",
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
        document3 = Document(
            core_id="doc3",
            core_profile_id="id3",
            core_title="sametitle1",
            core_type="conference_proceedings",
            core_created=datetime.now(),
            core_last_modified=datetime.now(),
            core_abstract="Newer abstract",
            core_source="Newer source",
            core_year=2015,
            core_authors=[],
            core_keywords=[],
            tags=[]
        )
        unified_document_title_to_documents = dict()
        unified_document_title_to_documents["samtetitle1"] = [document1, document3]
        unified_document_title_to_documents["title2"] = [document2]

        # Trigger cache document update
        data_controller.crawl_data.update_cache_documents(unified_document_title_to_documents)

        # Check data count in the table
        cnt = data_controller.engine.execute("SELECT COUNT(*) FROM cache_document").fetchone()
        self.assertEqual(cnt[0], 2)

        # Then query sametitle row
        id = generate_id('sametitle1')
        row = data_controller.engine.execute(
            "SELECT id, document_id, title "
            "FROM cache_document "
            "WHERE id='%s'" % id
        ).fetchone()
        self.assertEqual(row["id"], id)
        self.assertEqual(row["title"], "sametitle1")

        # Now update documents and check if the link is set correctly
        data_controller.crawl_data.update_documents([document1, document2, document3])
        row = data_controller.engine.execute(
            "SELECT cd.title as title "
            "FROM cache_document cd, document d "
            "WHERE cd.document_id = d.id "
            "AND cd.id='%s' " % id
        ).fetchone()
        self.assertEqual(row["title"], "sametitle1")

    def test_update_cache_profiles(self):
        sqlite_in_memory = SQLiteConfiguration("")
        data_controller = DataController(sqlite_in_memory)
        data_controller.run_schema()

        # The call shall not crash with empty input
        r = data_controller.crawl_data.update_cache_profiles(dict())
        self.assertIsNone(r)

        profile1 = Profile("id1", "Hans", "Mustermann", "Longer Real Name", "")
        profile2 = Profile("id2", "Max", "Mustermann", "", "")
        profile3 = Profile("id3", "Hans", "Mustermann", "", "")

        unified_name_to_profiles = dict()
        unified_name_to_profiles["hansmustermann"] = [profile1, profile3]
        unified_name_to_profiles["maxmustermann"] = [profile2]

        data_controller.crawl_data.update_cache_profiles(unified_name_to_profiles)

        # Check data count in the table
        cnt = data_controller.engine.execute("SELECT COUNT(*) FROM cache_profile").fetchone()
        self.assertEqual(cnt[0], 2)

        # Then query same title row
        id = generate_id('hansmustermann')
        row = data_controller.engine.execute(
            "SELECT id, profile_id, name "
            "FROM cache_profile "
            "WHERE id='%s'" % id
        ).fetchone()

        self.assertEqual(row["id"], id)
        self.assertEqual(row["name"], "Hans Mustermann")

        # Now update profiles and check if the link is set correctly
        data_controller.crawl_data.update_profiles([profile1, profile2, profile3])
        row = data_controller.engine.execute(
            "SELECT cp.name as name "
            "FROM cache_profile cp, profile p "
            "WHERE cp.profile_id = p.id "
            "AND cp.id='%s' " % id
        ).fetchone()
        self.assertEqual(row["name"], "Hans Mustermann")

    def test_update_cache_fields(self):
        sqlite_in_memory = SQLiteConfiguration("")
        data_controller = DataController(sqlite_in_memory)
        data_controller.run_schema()

        # The call shall not crash with empty input
        r = data_controller.crawl_data.update_cache_fields(dict())
        self.assertIsNone(r)

        field1 = CacheField(title="field 1", unified_title="field1")
        field2 = CacheField(title="field 2", unified_title="field2")
        unified_field_title_to_field = dict()
        unified_field_title_to_field["field1"] = field1
        unified_field_title_to_field["field2"] = field2

        data_controller.crawl_data.update_cache_fields(unified_field_title_to_field)

        # Check data count in the table
        cnt = data_controller.engine.execute("SELECT COUNT(*) FROM cache_field").fetchone()
        self.assertEqual(cnt[0], 2)

        # Then query rows
        id = generate_id('field1')
        row = data_controller.engine.execute(
            "SELECT id, title "
            "FROM cache_field "
            "WHERE id='%s' " % id
        ).fetchone()

        # Check first row
        self.assertEqual(row["id"], id)
        self.assertEqual(row['title'], "field 1")

    def test_link_profiles_to_documents(self):
        sqlite_in_memory = SQLiteConfiguration("")
        data_controller = DataController(sqlite_in_memory)
        data_controller.run_schema()

        # The call shall not crash with empty input
        r = data_controller.crawl_data.link_profiles_to_documents(dict(), dict(), dict())
        self.assertIsNone(r)

    def test_link_fields_to_documents(self):
        sqlite_in_memory = SQLiteConfiguration("")
        data_controller = DataController(sqlite_in_memory)
        data_controller.run_schema()

        # The call shall not crash with empty input
        r = data_controller.crawl_data.link_fields_to_documents(dict())
        self.assertIsNone(r)

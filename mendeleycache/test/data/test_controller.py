__author__ = 'kohn'

import unittest
from mendeleycache.data.controller import DataController
from mendeleycache.data.config import SQLiteConfiguration

from sqlalchemy.exc import DBAPIError

class TestDataController(unittest.TestCase):

    def test_errors(self):
        sqlite_in_memory = SQLiteConfiguration("sqlite", "")
        ctrl = DataController(sqlite_in_memory)

        # Try completely dumb sql
        try:
            with ctrl.engine.connect() as conn:
                conn.execute("COMPLETELY WRONG COMMAND")
                self.fail("DBAPI exception not fired")
        except DBAPIError as e:
            pass

    def test_run_schema(self):
        sqlite_in_memory = SQLiteConfiguration("sqlite", "")
        ctrl = DataController(sqlite_in_memory)

        # First check that none of the tables exists
        self.assertFalse(ctrl.table_exists('profile'))
        self.assertFalse(ctrl.table_exists('document'))
        self.assertFalse(ctrl.table_exists('cache_profile'))
        self.assertFalse(ctrl.table_exists('cache_document'))
        self.assertFalse(ctrl.table_exists('cache_field'))
        self.assertFalse(ctrl.table_exists('cache_document_has_cache_field'))
        self.assertFalse(ctrl.table_exists('cache_profile_has_cache_document'))
        self.assertFalse(ctrl.table_exists('document_access_log'))
        self.assertFalse(ctrl.table_exists('document_access_log_has_cache_document'))
        self.assertFalse(ctrl.table_exists('field_access_log'))
        self.assertFalse(ctrl.table_exists('field_access_log_has_cache_field'))

        # Create schema
        ctrl.run_schema()

        # After schema creation all tables need to exist
        self.assertTrue(ctrl.table_exists('profile'))
        self.assertTrue(ctrl.table_exists('document'))
        self.assertTrue(ctrl.table_exists('cache_profile'))
        self.assertTrue(ctrl.table_exists('cache_document'))
        self.assertTrue(ctrl.table_exists('cache_field'))
        self.assertTrue(ctrl.table_exists('cache_document_has_cache_field'))
        self.assertTrue(ctrl.table_exists('cache_profile_has_cache_document'))
        self.assertTrue(ctrl.table_exists('document_access_log'))
        self.assertTrue(ctrl.table_exists('document_access_log_has_cache_document'))
        self.assertTrue(ctrl.table_exists('field_access_log'))
        self.assertTrue(ctrl.table_exists('field_access_log_has_cache_field'))

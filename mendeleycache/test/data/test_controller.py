__author__ = 'kohn'

import unittest
from mendeleycache.data.controller import DataController, create_engine
from mendeleycache.config import SQLiteConfiguration

from sqlalchemy.exc import DBAPIError

class TestDataController(unittest.TestCase):

    def test_errors(self):
        sqlite_in_memory = SQLiteConfiguration("")
        ctrl = DataController(sqlite_in_memory)

        # Try completely dumb sql
        try:
            with ctrl.engine.connect() as conn:
                conn.execute("COMPLETELY WRONG COMMAND")
                self.fail("DBAPI exception not fired")
        except DBAPIError as e:
            pass

    def test_run_schema(self):
        sqlite_in_memory = SQLiteConfiguration("")
        ctrl = DataController(sqlite_in_memory)

        # First check that none of the tables exists
        self.assertFalse(ctrl.table_exists('profile'))
        self.assertFalse(ctrl.table_exists('document'))
        self.assertFalse(ctrl.table_exists('cache_profile'))
        self.assertFalse(ctrl.table_exists('cache_document'))
        self.assertFalse(ctrl.table_exists('cache_field'))
        self.assertFalse(ctrl.table_exists('cache_document_has_cache_field'))
        self.assertFalse(ctrl.table_exists('cache_profile_has_cache_document'))
        self.assertFalse(ctrl.table_exists('update_log'))

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
        self.assertTrue(ctrl.table_exists('update_log'))

    def test_is_initialized(self):
        sqlite_in_memory = SQLiteConfiguration("")
        ctrl = DataController(sqlite_in_memory)
        ctrl.run_schema()
        self.assertTrue(ctrl.is_initialized())

    def test_assert_drop(self):
        sqlite_in_memory = SQLiteConfiguration("")
        ctrl = DataController(sqlite_in_memory)
        ctrl.assert_schema()
        self.assertTrue(ctrl.is_initialized())
        ctrl.drop_all()
        self.assertFalse(ctrl.is_initialized())
        ctrl.assert_schema()
        self.assertTrue(ctrl.is_initialized())
        with ctrl.engine.begin() as conn:
            conn.execute("DROP TABLE cache_document")
        self.assertFalse(ctrl.is_initialized())
        ctrl.assert_schema()
        self.assertTrue(ctrl.is_initialized())

    def test_create_engine(self):
        sqlite_in_memory = SQLiteConfiguration("")

        engine = create_engine(sqlite_in_memory)
        self.assertIsNotNone(engine)

        # Option 1: Explicit connection
        conn = engine.connect()
        conn.execute("CREATE TABLE x (a INTEGER, b INTEGER)")
        conn.execute("INSERT INTO x (a, b) VALUES (1, 1)")
        conn.execute("INSERT INTO x (a, b) VALUES (2, 2)")
        result = conn.execute("SELECT x.a, x.b FROM x")
        conn.close()
        self.assertEqual(result.keys(), ["a", "b"])

        # Option 2: connect with statement
        with engine.connect() as conn:
            conn.execute("DELETE FROM x")
            conn.execute("INSERT INTO x (a, b) VALUES (42, 43)")
            results = conn.execute("SELECT x.a, x.b FROM x")
            for row in results:
                self.assertEqual(row['a'], 42)
                self.assertEqual(row['b'], 43)

        # Option 3: transaction with begin
        with engine.begin() as conn:
            conn.execute("DELETE FROM x")
            conn.execute("INSERT INTO x (a, b) VALUES (42, 43)")
            results = conn.execute("SELECT x.a, x.b FROM x")
            for row in results:
                self.assertEqual(row['a'], 42)
                self.assertEqual(row['b'], 43)


__author__ = 'kohn'

import unittest
from mendeleycache.data.config import create_engine
from mendeleycache.config import DatabaseConfiguration, SQLiteConfiguration, MySQLConfiguration


class TestConfig(unittest.TestCase):

    def test_create_engine(self):
        sqlite_in_memory = SQLiteConfiguration("sqlite", "")

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

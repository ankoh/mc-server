__author__ = 'kohn'

import unittest
from mendeleycache.data.config import create_engine
from mendeleycache.config import DatabaseConfiguration, SQLiteConfiguration, MySQLConfiguration


class TestConfig(unittest.TestCase):

    def test_create_engine(self):
        sqlite_in_memory = SQLiteConfiguration("sqlite", "")

        engine = create_engine(sqlite_in_memory)
        self.assertIsNotNone(engine)

        conn = engine.connect()
        conn.execute("CREATE TABLE x (a INTEGER, b INTEGER)")
        conn.execute("INSERT INTO x (a, b) VALUES (1, 1)")
        conn.execute("INSERT INTO x (a, b) VALUES (2, 2)")
        result = conn.execute("SELECT x.a, x.b FROM x")
        conn.close()

        assert result.keys() == ["a", "b"]

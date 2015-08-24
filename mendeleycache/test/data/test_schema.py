__author__ = 'kohn'

import unittest

from mendeleycache.data.schema import read_mysql_schema, read_sqlite_schema

class TestSchema(unittest.TestCase):

    def test_read_sqlite_schema(self):
        cmds = read_sqlite_schema()
        self.assertEqual(len(cmds), 23 + 1)

    def test_read_mysql_schema(self):
        cmds = read_mysql_schema()
        self.assertEqual(len(cmds), 23 + 1)
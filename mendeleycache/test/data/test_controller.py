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
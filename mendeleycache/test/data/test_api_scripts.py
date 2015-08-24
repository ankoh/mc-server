__author__ = 'kohn'

import unittest

from mendeleycache.config import SQLiteConfiguration
from mendeleycache.data.controller import DataController
from mendeleycache.data.api_scripts import ApiScripts


class TestApiScripts(unittest.TestCase):

    def test_get_profiles_by_profile_ids_or_field_ids(self):
        sqlite_in_memory = SQLiteConfiguration("sqlite", "")
        data_controller = DataController(sqlite_in_memory)
        api_scripts = ApiScripts(data_controller.engine)
        data_controller.run_schema()

        # The call shall not crash with empty input
        api_scripts.get_profiles_by_profile_ids_or_field_ids([], [])
        api_scripts.get_profiles_by_profile_ids_or_field_ids([42,43], [])
        api_scripts.get_profiles_by_profile_ids_or_field_ids([], [42,43])
        api_scripts.get_profiles_by_profile_ids_or_field_ids([42,43], [44,45])

    def test_get_documents_by_profile_ids_and_field_ids(self):
        sqlite_in_memory = SQLiteConfiguration("sqlite", "")
        data_controller = DataController(sqlite_in_memory)
        api_scripts = ApiScripts(data_controller.engine)
        data_controller.run_schema()

        # The call shall not crash with empty input
        api_scripts.get_documents_by_profile_ids_and_field_ids([], [])
        api_scripts.get_documents_by_profile_ids_and_field_ids([42,43], [])
        api_scripts.get_documents_by_profile_ids_and_field_ids([], [42,43])
        api_scripts.get_documents_by_profile_ids_and_field_ids([42,43], [44,45])

    def test_get_fields(self):
        sqlite_in_memory = SQLiteConfiguration("sqlite", "")
        data_controller = DataController(sqlite_in_memory)
        api_scripts = ApiScripts(data_controller.engine)
        data_controller.run_schema()

        # The call shall not crash with empty input
        api_scripts.get_fields()

    def test_get_profiles_slim(self):
        sqlite_in_memory = SQLiteConfiguration("sqlite", "")
        data_controller = DataController(sqlite_in_memory)
        api_scripts = ApiScripts(data_controller.engine)
        data_controller.run_schema()

        # The call shall not crash with empty input
        api_scripts.get_profiles_slim()


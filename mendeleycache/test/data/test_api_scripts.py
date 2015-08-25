__author__ = 'kohn'

import unittest

from mendeleycache.config import SQLiteConfiguration
from mendeleycache.data.controller import DataController
from mendeleycache.data.api_scripts import ApiScripts


class TestApiScripts(unittest.TestCase):

    def test_get_profiles_by_profile_ids_or_field_ids(self):
        sqlite_in_memory = SQLiteConfiguration("sqlite", "")
        data_controller = DataController(sqlite_in_memory)
        data_controller.run_schema()

        # The call shall not crash with empty input
        data_controller.api_data.get_profiles_by_profile_ids_or_field_ids([], [])
        data_controller.api_data.get_profiles_by_profile_ids_or_field_ids([42, 43], [])
        data_controller.api_data.get_profiles_by_profile_ids_or_field_ids([], [42, 43])
        data_controller.api_data.get_profiles_by_profile_ids_or_field_ids([42, 43], [44, 45])

    def test_get_documents_by_profile_ids_and_field_ids(self):
        sqlite_in_memory = SQLiteConfiguration("sqlite", "")
        data_controller = DataController(sqlite_in_memory)
        data_controller.run_schema()

        # The call shall not crash with empty input
        data_controller.api_data.get_documents_by_profile_ids_and_field_ids([], [])
        data_controller.api_data.get_documents_by_profile_ids_and_field_ids([42, 43], [])
        data_controller.api_data.get_documents_by_profile_ids_and_field_ids([], [42, 43])
        data_controller.api_data.get_documents_by_profile_ids_and_field_ids([42, 43], [44, 45])

    def test_get_fields(self):
        sqlite_in_memory = SQLiteConfiguration("sqlite", "")
        data_controller = DataController(sqlite_in_memory)
        data_controller.run_schema()

        # The call shall not crash with empty input
        data_controller.api_data.get_fields()

    def test_get_profiles_slim(self):
        sqlite_in_memory = SQLiteConfiguration("sqlite", "")
        data_controller = DataController(sqlite_in_memory)
        data_controller.run_schema()

        # The call shall not crash with empty input
        data_controller.api_data.get_profiles_slim()


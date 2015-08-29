__author__ = 'kohn'

import unittest

from mendeleycache.analyzer.controller import AnalysisController
from mendeleycache.crawler.controller import CrawlController
from mendeleycache.data.controller import DataController
from mendeleycache.crawler.file_crawler import FileCrawler
from mendeleycache.pipeline import PipelineController
from mendeleycache.config import SQLiteConfiguration



class TestApiScripts(unittest.TestCase):

    def test_get_profiles_by_profile_ids_or_field_ids(self):
        sqlite_in_memory = SQLiteConfiguration("")
        data_controller = DataController(sqlite_in_memory)
        data_controller.run_schema()

        # The call shall not crash with empty input
        data_controller.api_data.get_profiles_by_profile_ids_or_field_ids([], [])
        data_controller.api_data.get_profiles_by_profile_ids_or_field_ids([42, 43], [])
        data_controller.api_data.get_profiles_by_profile_ids_or_field_ids([], [42, 43])
        data_controller.api_data.get_profiles_by_profile_ids_or_field_ids([42, 43], [44, 45])

    def test_get_documents_by_profile_ids_and_field_ids(self):
        sqlite_in_memory = SQLiteConfiguration("")
        data_controller = DataController(sqlite_in_memory)
        data_controller.run_schema()

        # The call shall not crash with empty input
        data_controller.api_data.get_documents_by_profile_ids_and_field_ids([], [])
        data_controller.api_data.get_documents_by_profile_ids_and_field_ids([42, 43], [])
        data_controller.api_data.get_documents_by_profile_ids_and_field_ids([], [42, 43])
        data_controller.api_data.get_documents_by_profile_ids_and_field_ids([42, 43], [44, 45])

    def test_get_fields(self):
        sqlite_in_memory = SQLiteConfiguration("")
        data_controller = DataController(sqlite_in_memory)
        data_controller.run_schema()

        # The call shall not crash with empty input
        data_controller.api_data.get_fields()

    def test_get_profiles_slim(self):
        sqlite_in_memory = SQLiteConfiguration("")
        data_controller = DataController(sqlite_in_memory)
        data_controller.run_schema()

        # The call shall not crash with empty input
        data_controller.api_data.get_profiles_slim()

    def test_all_with_pipeline_data(self):
        sqlite_in_memory = SQLiteConfiguration("")
        data_controller = DataController(sqlite_in_memory)
        data_controller.run_schema()

        crawler = FileCrawler()
        crawl_controller = CrawlController(crawler, "d0b7f41f-ad37-3b47-ab70-9feac35557cc")

        analysis_controller = AnalysisController()

        pipeline_controller = PipelineController(
            data_controller=data_controller,
            crawl_controller=crawl_controller,
            analysis_controller=analysis_controller
        )

        # Clean run
        pipeline_controller.execute()

        # Test slim profiles
        slim_profiles = data_controller.api_data.get_profiles_slim()
        self.assertEqual(len(slim_profiles), 19)

        # Test fields
        fields = data_controller.api_data.get_fields()
        self.assertEqual(len(fields), 14)


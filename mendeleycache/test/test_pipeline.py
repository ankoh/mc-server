__author__ = 'kohn'

import unittest

from mendeleycache.analyzer.controller import AnalysisController
from mendeleycache.crawler.controller import CrawlController
from mendeleycache.crawler.file_crawler import FileCrawler
from mendeleycache.data.controller import DataController
from mendeleycache.pipeline import PipelineController
from mendeleycache.config import SQLiteConfiguration


class TestPipeline(unittest.TestCase):

    def test_execute(self):
        sqlite_in_memory = SQLiteConfiguration("sqlite", "")
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

        pipeline_controller.execute()

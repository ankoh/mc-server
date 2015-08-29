__author__ = 'kohn'

from mendeleycache.config import ServiceConfiguration
from mendeleycache.data.controller import DataController
from mendeleycache.crawler.file_crawler import FileCrawler
from mendeleycache.crawler.controller import CrawlController
from mendeleycache.analyzer.controller import AnalysisController
from mendeleycache.pipeline import PipelineController
from mendeleycache.logging import log
from mendeleycache.test.test_pipeline import sample_pipeline
from mendeleycache.test.routes.test_api import sample_api

import unittest
from unittest import TestLoader
from mendeleycache.utils.files import get_relative_path
import logging

import os
import sys

if len(sys.argv) >= 2:
    log.info("Welcome to the MendeleyCache runner")

    command = sys.argv[1]

    # Test runner
    if command == "tests":
        log.info("Disabling non-critical logs for better unittest output")

        # Disable logging for tests
        logging.disable(logging.CRITICAL)

        # Get project root path
        project_root = get_relative_path(".")

        # Prepare
        loader = TestLoader()
        runner = unittest.TextTestRunner(verbosity=2)

        # Create suites
        all = loader.discover(start_dir=project_root)

        # Run suites
        runner.run(all)

    # Pipeline runner
    elif command == "pipeline":
        config = ServiceConfiguration()
        config.load()

        data_controller = DataController(config.database)
        if not data_controller.is_initialized():
            log.critical("Database is not initialized")
            exit()

        crawler = FileCrawler()
        crawl_controller = CrawlController(crawler, config.crawler.research_group)
        analysis_controller = AnalysisController()
        pipeline_controller = PipelineController(
            data_controller=data_controller,
            crawl_controller=crawl_controller,
            analysis_controller=analysis_controller
        )
        pipeline_controller.execute()

    # Show file-crawler sample data
    elif command == "sample-pipeline":
        sample_pipeline()

    elif command == "sample-api":
        sample_api()

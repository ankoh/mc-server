__author__ = 'kohn'

from mendeleycache.config import ServiceConfiguration
from mendeleycache.data.controller import DataController
from mendeleycache.crawler.file_crawler import FileCrawler
from mendeleycache.crawler.controller import CrawlController
from mendeleycache.analyzer.controller import AnalysisController
from mendeleycache.pipeline import PipelineController
from mendeleycache.logging import log
from mendeleycache.utils.files import get_relative_path
from mendeleycache.test.test_pipeline import sample_pipeline
from mendeleycache.test.routes.test_api import sample_api

import unittest
from unittest import TestLoader

import logging
import sys
import os
import json
from pprint import PrettyPrinter


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

        crawler = None
        if not config.uses_mendeley:
            log.info("Pipeline uses FileCrawler")
            crawler = FileCrawler()
        else:
            from mendeleycache.crawler.sdk_crawler import SDKCrawler
            log.info("Pipeline uses SDKCrawler".format(
                app_id=config.crawler.app_id,
                app_secret=config.crawler.app_secret
            ))
            crawler = SDKCrawler(
                app_id=config.crawler.app_id,
                app_secret=config.crawler.app_secret
            )

        crawl_controller = CrawlController(crawler, config.crawler.research_group)
        analysis_controller = AnalysisController()
        pipeline_controller = PipelineController(
            data_controller=data_controller,
            crawl_controller=crawl_controller,
            analysis_controller=analysis_controller
        )
        pipeline_controller.execute()

    # Show file-crawler sample data
    elif command == "sample-file-pipeline":
        sample_pipeline()

    # Trigger the pipeline with the mendeley sdk crawler
    elif command == "sample-sdk-pipeline":
        if not len(sys.argv) >= 4:
            log.critical("Missing arguments: mendeleycache.runner sample-sdk-pipeline {app-id} {app-secret}")

        app_id = sys.argv[2]
        app_secret = sys.argv[3]
        os.environ["MC_CRAWLER"] = 'mendeley'
        os.environ["MC_APP_ID"] = app_id
        os.environ["MC_APP_SECRET"] = app_secret
        sample_pipeline(app_id=app_id, app_secret=app_secret)

    elif command == "sample-sdk-crawler":
        from mendeleycache.crawler.sdk_crawler import SDKCrawler
        if not len(sys.argv) >= 4:
            log.critical("Missing arguments: mendeleycache.runner sample-sdk-crawler {app-id} {app-secret}")
            exit(1)

        app_id = sys.argv[2]
        app_secret = sys.argv[3]
        group_id = "d0b7f41f-ad37-3b47-ab70-9feac35557cc"

        crawler = SDKCrawler(app_id=app_id, app_secret=app_secret)
        crawler.prepare()
        elements = crawler.get_documents_by_profile_id('a43c2a50-e164-3114-adb1-34d792c09268')
        crawler.destroy()

        pp = PrettyPrinter(indent=4)
        for elem in elements:
            pp.pprint(vars(elem))

    elif command == "sample-api":
        sample_api()

# Flask imports
from flask import Flask

# App imports
from mendeleycache.routes.fields import FieldsController
from mendeleycache.routes.profiles import ProfilesController
from mendeleycache.routes.publications import PublicationsController
from mendeleycache.routes.system import SystemController
from mendeleycache.config import ServiceConfiguration
from mendeleycache.data.controller import DataController
from mendeleycache.analyzer.controller import AnalysisController
from mendeleycache.crawler.file_crawler import FileCrawler
from mendeleycache.crawler.controller import CrawlController
from mendeleycache.pipeline import PipelineController
from mendeleycache.logging import log


class MendeleyCache(Flask):
    def __init__(self, *args, **kwargs):
        super(MendeleyCache, self).__init__(*args, **kwargs)

        # Read configuration
        self.configuration = ServiceConfiguration()
        self.configuration.load()

        # Create service controllers
        self.data_controller = DataController(self.configuration.database)
        self.data_controller.assert_schema()

        # TODO: read crawler type from config as well
        self.crawler = FileCrawler()
        self.crawl_controller = CrawlController(self.crawler, self.configuration.mendeley.research_group)
        self.analysis_controller = AnalysisController()
        self.pipeline_controller = PipelineController(
            data_controller=self.data_controller,
            crawl_controller=self.crawl_controller,
            analysis_controller=self.analysis_controller
        )

        # Create the routing controllers
        self.fields_controller = FieldsController(self, self.data_controller)
        self.profiles_controller = ProfilesController(self, self.data_controller)
        self.publications_controller = PublicationsController(self, self.data_controller)
        self.system_controller = SystemController(self, self.data_controller, self.configuration)

        # Register the routes
        self.register_routes()

        log.info("MendeleyCache initialized")

    def register_routes(self):
        self.fields_controller.register()
        self.profiles_controller.register()
        self.publications_controller.register()
        self.system_controller.register()

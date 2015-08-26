# Flask imports
from flask import Flask

# App imports
from mendeleycache.routes.fields import FieldsController
from mendeleycache.routes.profiles import ProfilesController
from mendeleycache.routes.publications import PublicationsController
from mendeleycache.routes.statistics import StatisticsController
from mendeleycache.routes.system import SystemController
from mendeleycache.config import ServiceConfiguration
from mendeleycache.data.controller import DataController
from mendeleycache.analyzer.controller import AnalysisController
from mendeleycache.crawler.file_crawler import FileCrawler
from mendeleycache.crawler.controller import CrawlController
from mendeleycache.pipeline import PipelineController


class MendeleyCache(Flask):
    def __init__(self, *args, **kwargs):
        super(MendeleyCache, self).__init__('mendeleycache', *args, **kwargs)

        # Read configuration
        # TODO: set the path to the config through environment variables and pass that as parameter
        self.configuration = ServiceConfiguration()
        self.configuration.load()

        # Create service controllers
        self.data_controller = DataController(self.configuration.database)
        # TODO: Only run schema if in debug or schema not existing (index collision)
        self.data_controller.run_schema()
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
        self.statistics_controller = StatisticsController(self, self.data_controller)
        self.system_controller = SystemController(self, self.data_controller, self.configuration)

        # Register the routes
        self.register_routes()

    def register_routes(self):
        self.fields_controller.register()
        self.profiles_controller.register()
        self.publications_controller.register()
        self.statistics_controller.register()
        self.system_controller.register()

# If entry point run the application
if __name__ == '__main__':
    # Initialize the main application
    app = MendeleyCache(__name__)
    app.run(debug=True)

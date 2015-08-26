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

# Initialize the main application
app = Flask(__name__)

# Read configuration
# TODO: set the path to the config through environment variables and pass that as parameter
config = ServiceConfiguration()
config.load()

# Create service controllers
data_controller = DataController(config.database)
# TODO: Only run schema if in debug or schema not existing (index collision)
data_controller.run_schema()
# TODO: read crawler type from config as well
crawler = FileCrawler()
crawl_controller = CrawlController(crawler, config.mendeley.research_group)
analysis_controller = AnalysisController()
pipeline_controller = PipelineController(
    data_controller=data_controller,
    crawl_controller=crawl_controller,
    analysis_controller=analysis_controller
)

# Create the routing controllers
fields_controller = FieldsController(app, data_controller)
profiles_controller = ProfilesController(app, data_controller)
publications_controller = PublicationsController(app, data_controller)
statistics_controller = StatisticsController(app, data_controller)
system_controller = SystemController(app, data_controller, config)

# Register the url handlers
fields_controller.register()
profiles_controller.register()
publications_controller.register()
statistics_controller.register()
system_controller.register()


# If entry point run the application
if __name__ == '__main__':
    app.run(debug=True)

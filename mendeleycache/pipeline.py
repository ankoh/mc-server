__author__ = 'kohn'

from mendeleycache.data.controller import DataController
from mendeleycache.crawler.controller import CrawlController
from mendeleycache.analyzer.controller import AnalysisController


class PipelineController:
    """
    The PipelineController manages the data flow.
    It triggers the CrawlController, passes the results to the AnalysisController
    and from there to the DataController
    """

    def __init__(self,
                 data_controller: DataController,
                 crawl_controller: CrawlController,
                 analysis_controller: AnalysisController):
        self._data_controller = data_controller
        self._crawl_controller = crawl_controller
        self._analysis_controller = analysis_controller

    def execute(self):
        """
        Execute a single run of the pipeline
        This is later scheduled like once per day
        :return:
        """
        self._crawl_controller.execute()
        profiles = self._crawl_controller.profiles
        profile_docs = self._crawl_controller.profile_documents
        group_docs = self._crawl_controller.group_documents

        self._analysis_controller.prepare(profiles, profile_docs, group_docs)
        self._analysis_controller.execute()

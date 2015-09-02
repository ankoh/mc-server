__author__ = 'kohn'

from mendeleycache.data.controller import DataController
from mendeleycache.crawler.controller import CrawlController
from mendeleycache.analyzer.controller import AnalysisController
from mendeleycache.logging import log


class PipelineReport:
    def __init__(self,
                 profiles: int,
                 documents: int,
                 unified_profiles: int,
                 unified_documents: int,
                 fields: int,
                 field_associations: int):
        self.profiles = profiles
        self.documents = documents
        self.unified_profiles = unified_profiles
        self.unified_documents = unified_documents
        self.fields = fields
        self.field_associations = field_associations


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

        # Run the crawler
        self._crawl_controller.execute()

        # Crawl results
        profiles = self._crawl_controller.profiles
        profile_docs = self._crawl_controller.profile_documents
        group_docs = self._crawl_controller.group_documents

        # Then pipe the data to the analysis controller
        self._analysis_controller.prepare(profiles, profile_docs, group_docs)
        self._analysis_controller.execute()

        # Analysis results
        documents = self._analysis_controller.documents
        unified_name_to_profiles = self._analysis_controller.unified_name_to_profiles
        unified_document_title_to_documents = self._analysis_controller.unified_document_title_to_documents
        unified_field_title_to_field = self._analysis_controller.unified_field_title_to_field
        unified_field_title_to_documents = self._analysis_controller.unified_field_title_to_documents
        unified_name_to_authored_documents = self._analysis_controller.unified_name_to_authored_documents
        unified_name_to_participated_documents = self._analysis_controller.unified_name_to_participated_documents

        # Then store the all data with the data controller
        self._data_controller.crawl_data.execute(
            profiles=profiles,
            documents=documents,
            unified_name_to_profiles=unified_name_to_profiles,
            unified_document_title_to_documents=unified_document_title_to_documents,
            unified_field_title_to_field=unified_field_title_to_field,
            unified_field_title_to_documents=unified_field_title_to_documents,
            unified_name_to_authored_documents=unified_name_to_authored_documents,
            unified_name_to_participated_documents=unified_name_to_participated_documents
        )

        # Count field associations
        field_associations = 0
        for title, docs in unified_field_title_to_documents.items():
            field_associations += len(docs)

        # Generate report
        report = PipelineReport(
            profiles=len(profiles),
            documents=len(documents),
            unified_profiles=len(unified_name_to_profiles),
            unified_documents=len(unified_document_title_to_documents),
            fields=len(unified_field_title_to_field),
            field_associations=field_associations
        )

        # Log report
        log.info("Pipeline has been executed\n"
                 "\t| replaced {profiles} profiles\n"
                 "\t| replaced {documents} documents\n"
                 "\t| replaced {unified_profiles} unified profile names\n"
                 "\t| replaced {unified_documents} unified document titles\n"
                 "\t| replaced {fields} research fields\n"
                 "\t| replaced {field_associations} field associations\n".format(
                profiles=report.profiles,
                documents=report.documents,
                unified_profiles=report.unified_profiles,
                unified_documents=report.unified_documents,
                fields=report.fields,
                field_associations=report.field_associations
            )
        )

        # Return report
        return report

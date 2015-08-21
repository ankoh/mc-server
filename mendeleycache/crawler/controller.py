__author__ = 'kohn'

from mendeleycache.crawler.abstract_crawler import AbstractCrawler
from mendeleycache.config import ServiceConfiguration
from queue import Queue
from threading import Thread

# number of workers that are used to fetch the publications & profiles in parallel
number_workers = 4


class CrawlerController:
    """
    The crawler controller spawns mutliple crawlers and returns the results afterwards
    """
    def __init__(self, config: ServiceConfiguration, crawler: AbstractCrawler):
        self.__research_group = config.mendeley.research_group
        self.__crawler = crawler

        self.__members = []
        self.__profiles = dict()
        self.__profile_documents = dict()
        self.__group_documents = []
        self.__succeeded = False

    @property
    def members(self):
        return self.__members

    @property
    def profiles(self):
        return self.__profiles

    @property
    def profile_documents(self):
        return self.__profile_documents

    @property
    def group_documents(self):
        return self.__group_documents

    @property
    def succeeded(self):
        return self.__succeeded

    # Worker queue
    __profile_id_queue = Queue()

    def profile_id_worker(self):
        """
        Given a prefilled queue with profile ids this worker will
        pop an id and fetch profile and documents
        :return:
        """
        while not self.__profile_id_queue.empty():
            profile_id = self.__profile_id_queue.get()
            # Fetch the profile
            profile = self.__crawler.get_profile_by_id(profile_id)
            self.__profiles[profile_id] = profile
            # Fetch the document
            documents = self.__crawler.get_documents_by_profile_id(profile_id)
            self.__profile_documents[profile_id] = documents
            # Mark task as done
            self.__profile_id_queue.task_done()

            # DEBUG
            print(profile_id + " fetched")

    def crawl_group_members(self):
        """
        Fetches members of the pre-configured research group
        :return:
        """
        self.__members = self.__crawler.get_group_members(self.__research_group)

    def crawl_profiles(self):
        """
        Given a populated members array this function crawls the profiles linked to the ids as well as the publications
        :return:
        """
        for member in self.__members:
            self.__profile_id_queue.put(member.profile_id)

        for i in range(number_workers):
            t = Thread(target=self.profile_id_worker)
            t.daemon = False
            t.start()

        # Wait for all workers to complete
        self.__profile_id_queue.join()

    def crawl_group_documents(self):
        """
        Fetches the publications that are associated with the pre-configured group
        :return:
        """
        self.__group_publications = self.__crawler.get_documents_by_group_id(self.__research_group)

    def crawl_all(self):
        """
        Subsequently trigger crawler for members, group_publications and profiles
        :return:
        """
        self.__succeeded = False
        self.crawl_group_members()
        self.crawl_group_documents()
        self.crawl_profiles()
        self.__succeeded = True

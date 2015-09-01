_author_ = 'kohn'

from mendeleycache.crawler.abstract_crawler import AbstractCrawler
from mendeleycache.config import ServiceConfiguration
from mendeleycache.models import Member, Profile, Document
from mendeleycache.logging import log
from queue import Queue
from threading import Thread
import traceback

# number of workers that are used to fetch the publications & profiles in parallel
number_profile_workers = 10
number_document_workers = 10


class CrawlController:
    """
    The crawler controller spawns mutliple crawlers and returns the results afterwards
    """
    def __init__(self, crawler: AbstractCrawler, research_group: str):
        self._research_group = research_group
        self._crawler = crawler

        self._members = []
        self._profiles = []
        self._profile_documents = dict()
        self._group_documents = []
        self._succeeded = False

    @property
    def members(self) -> [Member]:
        return self._members

    @property
    def profiles(self) -> [Profile]:
        return self._profiles

    @property
    def profile_documents(self) -> {}:
        return self._profile_documents

    @property
    def group_documents(self) -> {}:
        return self._group_documents

    @property
    def succeeded(self) -> bool:
        return self._succeeded

    # Worker queues
    _profile_queue = Queue()
    _profile_documents_queue = Queue()

    def profile_worker(self):
        """
        Given a prefilled profile queue this worker will pop an id
        and fetch the associated profile
        :return:
        """
        while not self._profile_queue.empty():
            profile_id = self._profile_queue.get()
            try:
                # Fetch the profile
                profile = self._crawler.get_profile_by_id(profile_id)
                self._profiles.append(profile)
                log.debug("The profile for profile_id {profile_id} has been fetched".format(
                    profile_id=profile_id
                ))
                # Mark task as done
                self._profile_queue.task_done()
            except Exception as e:
                log.warn("Failed to fetch the profile for profile_id {profile_id}".format(
                    profile_id=profile_id
                ))
                self._profile_queue.task_done()

    def document_worker(self):
        """
        Given a prefilled profile_documents queue this worker will pop an id
        and fetch the associated documents
        :return:
        """
        while not self._profile_documents_queue.empty():
            profile_id = self._profile_documents_queue.get()
            try:
                # Fetch the document
                documents = self._crawler.get_documents_by_profile_id(profile_id)
                self._profile_documents[profile_id] = documents
                log.debug("{num} documents have been fetched for profile_id {profile_id}".format(
                    num=len(documents),
                    profile_id=profile_id
                ))
                # Mark task as done
                self._profile_documents_queue.task_done()
            except Exception as e:
                log.warn("Failed to fetch documents for profile_id {profile_id}".format(
                    profile_id=profile_id
                ))
                self._profile_documents_queue.task_done()

    def crawl_group_members(self):
        """
        Fetches members of the pre-configured research group
        :return:
        """
        self._members = self._crawler.get_group_members(self._research_group)
        log.debug("{num} group members have been fetched for group_id {group_id}".format(
            num=len(self._members),
            group_id=self._research_group
        ))
        log.info("Group members have been fetched")

    def crawl_profiles(self):
        """
        Given a populated members array this function crawls the profiles linked to the ids as well as the publications
        :return:
        """
        log.debug("Adding members to worker queues")
        for member in self._members:
            self._profile_queue.put(member.profile_id)
            self._profile_documents_queue.put(member.profile_id)

        # Create profile crawlers
        log.debug("Spawning profile workers")
        for i in range(number_profile_workers):
            t = Thread(target=self.profile_worker)
            t.daemon = False
            t.start()

        # Create document crawlers
        log.debug("Spawning document crawlers")
        for i in range(number_document_workers):
            t = Thread(target=self.document_worker)
            t.daemon = False
            t.start()

        # Wait for both queues to complete
        self._profile_queue.join()
        self._profile_documents_queue.join()
        log.info("Profiles and associated documents have been fetched")

    def crawl_group_documents(self):
        """
        Fetches the publications that are associated with the pre-configured group
        :return:
        """
        self._group_documents = self._crawler.get_documents_by_group_id(self._research_group)
        log.debug("{num} documents have been fetched for group_id {group_id}".format(
            num=len(self._group_documents),
            group_id=self._research_group
        ))
        log.info("Group documents have been fetched")

    def reset(self):
        """
        Resets the state of the controller
        :return:
        """
        self._members = []
        self._profiles = []
        self._profile_documents = dict()
        self._group_documents = []
        self._succeeded = False

    def execute(self):
        """
        Subsequently trigger crawler for members, group_publications and profiles
        :return:
        """

        log.info("Crawler has been started")
        self.reset()
        self._crawler.prepare()
        self.crawl_group_members()
        self.crawl_group_documents()
        self.crawl_profiles()
        self._crawler.destroy()
        self._succeeded = True
        log.info("Crawler has been executed")

__author__ = 'kohn'

from mendeleycache.models import *
from abc import ABCMeta
from abc import abstractmethod


class AbstractCrawler(metaclass=ABCMeta):
    """
        The MendeleyCrawler is an abstract base class that describes
        the functionality to access (Publication-)Documents, (User-)Profiles and (Research-)Groups
    """

    @abstractmethod
    def get_group_members(self, group_id: str) -> [Member]:
        """
        get_group_members fetches all member ids of a given research group
        :param group_id: string id of the group that shall be queried for members
        :return: json object that contains all group member ids
        """
        pass

    @abstractmethod
    def get_profile_by_id(self, profile_id: str) -> Profile:
        """
        get_profile_by_id returns a user profile given a profile_id
        :param profile_id: id of the user profile
        :return: json object that represents the user profile
        """
        pass

    @abstractmethod
    def get_documents_by_profile_id(self, profile_id: str) -> [Document]:
        """
        get_documents_by_profile_id returns documents given a profile_id and whether the document shall be loaded completely
        :param profile_id: id of the user profile
        :return:
        """
        pass

    @abstractmethod
    def get_documents_by_group_id(self, group_id: str) -> [Document]:
        """
        get_documents_by_group_id returns documents given a group_id and whether the document shall be loaded completely
        :param group_id: id of the research group
        :return:
        """
        pass

    @abstractmethod
    def prepare(self):
        """
        Prepares the crawler for incoming requests (such as initializing an sdk session)
        :return:
        """
        pass

    @abstractmethod
    def destroy(self):
        """
        Destroys all objects when finished
        :return:
        """
        pass
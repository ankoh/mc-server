__author__ = 'kohn'

from os.path import exists
import logging

from mendeleycache.crawler.abstract_crawler import AbstractCrawler
from mendeleycache.crawler.json import get_document_from_json, get_members_from_json, get_profile_from_json
from mendeleycache.models import *
from mendeleycache.utils.files import get_relative_path
from mendeleycache.utils.validator import is_valid_mendeley_id
import json


class FileCrawler(AbstractCrawler):
    """
    The FileCrawler is a subclass of MendeleyCrawler and shall be used as Stub
    for the Mendeley API during the client Protractor tests
    """

    def get_group_members(self, group_id: str) -> [Member]:
        if not is_valid_mendeley_id(group_id):
            return []

        # Construct a file path relative to the project root
        path = get_relative_path('test', 'samples', 'groups', '%s.json' % group_id)

        # Check if path exists
        if not exists(path):
            return []

        # If yes open and parse json
        with open(path, 'r') as json_file:
            json_data = json.load(json_file)
            return get_members_from_json(json_data)

    def get_profile_by_id(self, profile_id: str) -> Profile:
        """
        Get profile object by profile_id
        :param profile_id:
        :return:
        """
        if not is_valid_mendeley_id(profile_id):
            return None

        # Construct a file path relative to the project root
        path = get_relative_path('test', 'samples', 'profiles', '%s.json' % profile_id)

        # Check if path exists
        if not exists(path):
            return None

        # If yes open and parse json
        with open(path, 'r') as json_file:
            json_data = json.load(json_file)
            return get_profile_from_json(json_data)

    def get_documents_by_profile_id(self, profile_id: str) -> [Document]:
        """
        Get document object by profile_id
        :param profile_id:
        :param all_view:
        :return:
        """
        if not is_valid_mendeley_id(profile_id):
            return None

        results = []

        # Construct a file path relative to the project root
        path = get_relative_path('test', 'samples', 'documents', 'by_profile_id', '%s.json' % profile_id)

        # Check if path exists
        if not exists(path):
            return []

        # If yes open and parse json
        with open(path, 'r') as json_file:
            json_data = json.load(json_file)

            for json_doc in json_data:
                doc = get_document_from_json(json_doc)
                results.append(doc)

        return results

    def get_documents_by_group_id(self, group_id: str) -> [Document]:
        """
        Get document object by profile_id
        :param profile_id:
        :param all_view:
        :return:
        """
        if not is_valid_mendeley_id(group_id):
            return None

        results = []

        # Construct a file path relative to the project root
        path = get_relative_path('test', 'samples', 'documents', 'by_group_id', '%s.json' % group_id)

        # Check if path exists
        if not exists(path):
            return []

        # If yes open and parse json
        with open(path, 'r') as json_file:
            json_data = json.load(json_file)

            for json_doc in json_data:
                doc = get_document_from_json(json_doc)
                results.append(doc)

        return results

    def prepare(self):
        pass

    def destroy(self):
        pass

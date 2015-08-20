__author__ = 'kohn'

from os.path import exists
from dateutil.parser import parse
import logging

from mendeleycache.crawler.mendeley_crawler import MendeleyCrawler
from mendeleycache.models import *
from mendeleycache.utils.files import get_path
from mendeleycache.utils.validator import is_valid_mendeley_id
import json
import pprint


class FileCrawler(MendeleyCrawler):
    """
    The FileCrawler is a subclass of MendeleyCrawler and shall be used as Stub
    for the Mendeley API during the client Protractor tests
    """

    def get_group_members(self, group_id: str) -> [Member]:
        if not is_valid_mendeley_id(group_id):
            return []

        result = []

        # Construct a file path relative to the project root
        path = get_path('test', 'data', 'groups', '%s.json' % group_id)

        # Check if path exists
        if not exists(path):
            return []

        # If yes open and parse json
        with open(path) as json_file:
            json_data = json.load(json_file)

            # Now iterate over the list and create new members
            for member in json_data:
                identifier = member['profile_id']
                role = member['role']
                joined = parse(member['joined'])
                result.append(Member(identifier, joined, role))

        # Return results
        return result

    def get_profile_by_id(self, profile_id: str) -> Profile:
        if not is_valid_mendeley_id(profile_id):
            return None

        # Construct a file path relative to the project root
        path = get_path('test', 'data', 'profiles', '%s.json' % profile_id)

        # Check if path exists
        if not exists(path):
            return None

        # If yes open and parse json
        with open(path) as json_file:
            json_data = json.load(json_file)

            identifier = json_data['id']
            first_name = json_data['first_name']
            last_name = json_data['last_name']
            display_name = json_data['display_name']
            link = json_data['link']

            return Profile(identifier, first_name, last_name, display_name, link)

        # Could not parse json file
        return None

    def get_documents_by_profile_id(self, profile_id: str, all_view: bool) -> [Document]:
        pass

    def get_documents_by_group_id(self, group_id: str, all_view: bool) -> [Document]:
        pass
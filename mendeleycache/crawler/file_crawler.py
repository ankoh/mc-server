__author__ = 'kohn'

import os.path
from dateutil.parser import parse

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
        with open(path) as json_file:
            json_data = json.load(json_file)

            # Now iterate over the list and create new members

            for member in json_data:
                id = member['profile_id']
                role = member['role']
                joined = parse(member['joined'])
                result.append(Member(id, joined, role))

        return result

    def get_profile_by_id(self, profile_id: str) -> Profile:
        pass

    def get_documents_by_profile_id(self, profile_id: str, all_view: bool) -> [Document]:
        pass

    def get_documents_by_group_id(self, group_id: str, all_view: bool) -> [Document]:
        pass
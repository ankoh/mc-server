__author__ = 'kohn'

from os.path import exists
from dateutil.parser import parse
import logging

from mendeleycache.crawler.mendeley_crawler import MendeleyCrawler
from mendeleycache.models import *
from mendeleycache.utils.files import get_path
from mendeleycache.utils.reflection import get_class_attributes, get_string_value_if_key_exists, get_dict_if_key_exists
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
        """
        Get profile object by profile_id
        :param profile_id:
        :return:
        """
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

    def get_document_from_json(self, json_doc) -> Document:
        """
        Given a json object return a Document object
        :param json_doc:
        :return:
        """
        # Core attributes
        core_id = json_doc['id']
        core_profile_id = json_doc['profile_id']
        core_title = json_doc['title']
        core_type = json_doc['type']
        core_created = parse(json_doc['created'])
        core_last_modified = parse(json_doc['last_modified'])
        core_year = int(json_doc['year'])
        core_abstract = get_string_value_if_key_exists(json_doc, 'abstract')
        core_source = get_string_value_if_key_exists(json_doc, 'source')

        # Core tuples
        core_authors = []
        core_keywords = []
        tags = []

        for author in get_dict_if_key_exists(json_doc, 'authors'):
            first_name = get_string_value_if_key_exists(author, 'first_name')
            last_name = get_string_value_if_key_exists(author, 'last_name')
            core_authors.append((first_name, last_name))

        for keyword in get_dict_if_key_exists(json_doc, 'keywords'):
            core_keywords.append(keyword)

        for tag in get_dict_if_key_exists(json_doc, 'tags'):
            tags.append(tag)

        # Append new document to result list
        return Document(
            core_id=core_id,
            core_profile_id=core_profile_id,
            core_title=core_title,
            core_type=core_type,
            core_created=core_created,
            core_last_modified=core_last_modified,
            core_abstract=core_abstract,
            core_source=core_source,
            core_year=core_year,
            core_authors=core_authors,
            core_keywords=core_keywords,
            tags=tags
        )

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
        path = get_path('test', 'data', 'documents', 'by_profile_id', '%s.json' % profile_id)

        # Check if path exists
        if not exists(path):
            return []

        # If yes open and parse json
        with open(path) as json_file:
            json_data = json.load(json_file)

            for json_doc in json_data:
                doc = self.get_document_from_json(json_doc)
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
        path = get_path('test', 'data', 'documents', 'by_group_id', '%s.json' % group_id)

        # Check if path exists
        if not exists(path):
            return []

        # If yes open and parse json
        with open(path) as json_file:
            json_data = json.load(json_file)

            for json_doc in json_data:
                doc = self.get_document_from_json(json_doc)
                results.append(doc)

        return results

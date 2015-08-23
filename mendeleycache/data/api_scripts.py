__author__ = 'kohn'

from sqlalchemy.engine import Engine
from sqlalchemy.sql import text

from mendeleycache.utils.files import get_relative_path
from mendeleycache.utils.regex import sql_comments

import textwrap
import re


class ApiScripts:
    def __init__(self, engine: Engine):
        self._engine = engine

        self._query_fields = ""
        self._query_profiles_slim = ""
        self._query_documents_by_profile_ids_and_field_ids = ""
        self._query_profiles_by_profile_ids_or_field_ids = ""
        self.read_sql()

    def read_sql(self):
        """
        Read the sql files and load them into the class variables
        :return:
        """
        path = get_relative_path('sql', 'api', 'query_fields.sql')
        with open(path, "r") as sql_file:
            sql = sql_file.read().replace(';', ' ')
            self._query_fields = re.sub(sql_comments, ' ', sql)

        path = get_relative_path('sql', 'api', 'query_profiles_slim.sql')
        with open(path, "r") as sql_file:
            sql = sql_file.read().replace(';', ' ')
            self._query_profiles_slim = re.sub(sql_comments, ' ', sql)

        # query_documents_by_profile_ids_and_field_ids
        path = get_relative_path('sql', 'api', 'query_documents_by_profile_ids_and_field_ids.sql')
        with open(path, "r") as sql_file:
            sql = sql_file.read().replace(';', ' ')
            self._query_documents_by_profile_ids_and_field_ids = re.sub(sql_comments, ' ', sql)

        # profiles_by_profile_ids_or_field_ids
        path = get_relative_path('sql', 'api', 'query_profiles_by_profile_ids_or_field_ids.sql')
        with open(path, "r") as sql_file:
            sql = sql_file.read().replace(';', ' ')
            self._query_profiles_by_profile_ids_or_field_ids = re.sub(sql_comments, ' ', sql)

    def get_documents_by_profile_ids_and_field_ids(self, profile_ids: [int], field_ids: [int]):
        """
        Given profile ids and field ids, queries all documents that belong to the research field
        AND are associated with these profiles
        :return:
        """
        query = text(self._query_documents_by_profile_ids_and_field_ids)
        return self._engine.execute(query, field_ids=field_ids, profile_ids=profile_ids).fetchall()

    def get_profiles_slim(self):
        """
        Query slim profiles for fast UI autocompletion
        :param profile_ids:
        :return:
        """
        query = text(self._query_profiles_slim)
        return self._engine.execute(query).fetchall()

    def get_profiles_by_profile_ids_or_field_ids(self, profile_ids: [int], field_ids: [int]):
        """
        Given a list of profile ids and field ids, queries all profiles that belong to the research field
        OR are associated with the profile_ids.
        :param slim:
        :return:
        """
        query = text(self._query_profiles_by_profile_ids_or_field_ids)
        return self._engine.execute(query, field_ids=field_ids, profile_ids=profile_ids).fetchall()

    def get_fields(self):
        """
        Queries all research fields
        :return:
        """
        query = text(self._query_fields)
        return self._engine.execute(query).fetchall()


    def get_general_statistics(self):
        """
        Queries the access logs to get the statistics of the past seven weeks (grouped by week)
        :return:
        """
        pass

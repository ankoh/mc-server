__author__ = 'kohn'

from sqlalchemy.engine import Engine

from mendeleycache.data.reader import read_sql_statements


import re

"""
ATTENTION: Apparently text() does not support lists in the in statement.
I'll build the statement myself and take care of sql injections.
For api_data.py that's still pretty straight forward.

The limitation arises in the DBAPI that SQLALCHEMY uses:
http://stackoverflow.com/questions/14512228/sqlalchemy-raw-sql-parameter-substitution-with-an-in-clause
"""


class ApiData:
    def __init__(self, engine: Engine):
        self._engine = engine

        self._query_fields =\
            read_sql_statements('sql', 'api', 'query_fields.sql')
        self._query_profiles_slim =\
            read_sql_statements('sql', 'api', 'query_profiles_slim.sql')
        self._query_documents_by_profile_ids_and_field_ids =\
            read_sql_statements('sql', 'api', 'query_documents_by_profile_ids_and_field_ids.sql')
        self._query_profiles_by_profile_ids_or_field_ids =\
            read_sql_statements('sql', 'api', 'query_profiles_by_profile_ids_or_field_ids.sql')

    def get_documents_by_profile_ids_and_field_ids(self, profile_ids: [int], field_ids: [int]):
        """
        Given profile ids and field ids, queries all documents that belong to the research field
        AND are associated with these profiles
        :return:
        """
        profile_ids_string = '(%s)' % (','.join(map(str, profile_ids)))
        field_ids_string = '(%s)' % (','.join(map(str, field_ids)))
        query = self._query_documents_by_profile_ids_and_field_ids[0]
        query = re.sub(':profile_ids', profile_ids_string, query)
        query = re.sub(':field_ids', field_ids_string, query)

        # Fire the sql script in a transaction
        with self._engine.begin() as conn:
            return conn.execute(query).fetchall()

    def get_profiles_slim(self):
        """
        Query slim profiles for fast UI auto completion
        :param profile_ids:
        :return:
        """
        query = self._query_profiles_slim[0]
        return self._engine.execute(query).fetchall()

    def get_profiles_by_profile_ids_or_field_ids(self, profile_ids: [int], field_ids: [int]):
        """
        Given a list of profile ids and field ids, queries all profiles that belong to the research field
        OR are associated with the profile_ids.
        :param slim:
        :return:
        """
        profile_ids_string = '(%s)' % (','.join(map(str, profile_ids)))
        field_ids_string = '(%s)' % (','.join(map(str, field_ids)))
        query = self._query_profiles_by_profile_ids_or_field_ids[0]
        query = re.sub(':profile_ids', profile_ids_string, query)
        query = re.sub(':field_ids', field_ids_string, query)

        # Fire the sql script in a transaction
        with self._engine.begin() as conn:
            return conn.execute(query).fetchall()

    def get_fields(self):
        """
        Queries all research fields
        :return:
        """
        query = self._query_fields[0]

        # Fire the sql script in a transaction
        with self._engine.begin() as conn:
            return conn.execute(query).fetchall()


    def get_general_statistics(self):
        """
        Queries the access logs to get the statistics of the past seven weeks (grouped by week)
        :return:
        """
        pass

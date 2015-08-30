__author__ = 'kohn'

from sqlalchemy.engine import Engine

from mendeleycache.data.reader import read_sql_statements
from mendeleycache.logging import log


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
        self._query_entities =\
            read_sql_statements('sql', 'api', 'query_entities.sql')

    def get_entities(self):
        """
        Returns the number of elements in each table
        :return:
        """
        query = self._query_entities[0]

        log.info("Querying entity numbers")

        # Fire the sql script in a transaction
        with self._engine.begin() as conn:
            return conn.execute(query).fetchall()


    def get_documents_by_profile_ids_and_field_ids(self, profile_ids: [int], field_ids: [int]):
        """
        Given profile ids and field ids, queries all documents that belong to the research field
        AND are associated with these profiles
        :return:
        """
        profile_ids_string = ""
        field_ids_string = ""
        if len(profile_ids) > 0:
            profile_ids_string = "(%s)" % (",".join(map(lambda x: "'%s'" % x, profile_ids)))
        else:
            profile_ids_string = "(NULL)"

        if len(field_ids) > 0:
            field_ids_string = "(%s)" % (",".join(map(lambda x: "'%s'" % x, field_ids)))
        else:
            field_ids_string = "(NULL)"

        query = self._query_documents_by_profile_ids_and_field_ids[0]
        query = re.sub(':profile_ids', profile_ids_string, query)
        query = re.sub(':field_ids', field_ids_string, query)

        log.info("Querying documents by profile_ids and field_ids\n"
                 "\t| profile_ids: {profile_ids}\n"
                 "\t| field_ids: {field_ids}\n".format(
            profile_ids=profile_ids_string,
            field_ids=field_ids_string
        ))

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

        log.info("Querying slim profiles")

        return self._engine.execute(query).fetchall()

    def get_profiles_by_profile_ids_or_field_ids(self, profile_ids: [int], field_ids: [int]):
        """
        Given a list of profile ids and field ids, queries all profiles that belong to the research field
        OR are associated with the profile_ids.
        :param slim:
        :return:
        """
        profile_ids_string = ""
        field_ids_string = ""
        if len(profile_ids) > 0:
            profile_ids_string = "(%s)" % (",".join(map(lambda x: "'%s'" % x, profile_ids)))
        else:
            profile_ids_string = "(NULL)"

        if len(field_ids) > 0:
            field_ids_string = "(%s)" % (",".join(map(lambda x: "'%s'" % x, field_ids)))
        else:
            field_ids_string = "(NULL)"

        query = self._query_profiles_by_profile_ids_or_field_ids[0]
        query = re.sub(':profile_ids', profile_ids_string, query)
        query = re.sub(':field_ids', field_ids_string, query)

        log.info("Querying profiles by profile_ids and field_ids\n"
                 "\t| profile_ids: {profile_ids}\n"
                 "\t| field_ids: {field_ids}\n".format(
            profile_ids=profile_ids_string,
            field_ids=field_ids_string
        ))

        # Fire the sql script in a transaction
        with self._engine.begin() as conn:
            return conn.execute(query).fetchall()

    def get_fields(self):
        """
        Queries all research fields
        :return:
        """
        query = self._query_fields[0]

        log.info("Querying fields")

        # Fire the sql script in a transaction
        with self._engine.begin() as conn:
            return conn.execute(query).fetchall()

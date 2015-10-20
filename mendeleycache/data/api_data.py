__author__ = 'kohn'

from sqlalchemy.engine import Engine
from mendeleycache.config import CacheConfiguration

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

query_head = re.compile("SELECT([A-Za-z0-9_., \n]+)FROM")


class ApiData:
    def __init__(self, engine: Engine):
        self._engine = engine

        self._query_fields =\
            read_sql_statements('sql', 'api', 'query_fields.sql')
        self._query_profiles_slim =\
            read_sql_statements('sql', 'api', 'query_profiles_slim.sql')
        self._query_all_documents =\
            read_sql_statements('sql', 'api', 'query_all_documents.sql')
        self._query_documents_by_profile_ids =\
            read_sql_statements('sql', 'api', 'query_documents_by_profile_ids.sql')
        self._query_documents_by_field_ids =\
            read_sql_statements('sql', 'api', 'query_documents_by_field_ids.sql')
        self._query_documents_by_profile_ids_and_field_ids =\
            read_sql_statements('sql', 'api', 'query_documents_by_profile_ids_and_field_ids.sql')
        self._query_profiles_by_profile_ids_or_field_ids =\
            read_sql_statements('sql', 'api', 'query_profiles_by_profile_ids_or_field_ids.sql')
        self._query_entities =\
            read_sql_statements('sql', 'api', 'query_entities.sql')
        self._query_last_update=\
            read_sql_statements('sql', 'api', 'query_last_update.sql')
        self._query_profile=\
            read_sql_statements('sql', 'api', 'query_profile.sql')

    def get_last_update(self):
        """
        Returns the last entry of the update_log
        :return:
        """
        query = self._query_last_update[0]
        log.info("Querying last update")

        with self._engine.begin() as conn:
            return conn.execute(query).fetchall()

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

    def get_documents_by_profile_ids_and_field_ids(self,
                                                   profile_ids: [int], field_ids: [int],
                                                   order_attr: str="year", order_dir: str="desc",
                                                   limit: int=0, offset: int=0, only_count: bool=False):
        """
        Given profile ids and field ids, queries all documents that belong to the research field
        AND are associated with these profiles
        :return:
        """

        profile_ids_string = ""
        field_ids_string = ""
        query_limit = 20
        query_offset = 0
        query_order_attr = "pub_year"
        query_order_dir = "ASC"
        if len(profile_ids) > 0:
            profile_ids_string = "(%s)" % (",".join(map(lambda x: "'%s'" % x, profile_ids)))
        else:
            profile_ids_string = "(NULL)"

        if len(field_ids) > 0:
            field_ids_string = "(%s)" % (",".join(map(lambda x: "'%s'" % x, field_ids)))
        else:
            field_ids_string = "(NULL)"

        # Check order attribute parameter
        if order_attr == "year":
            query_order_attr = "d.pub_year"
        elif order_attr == "title":
            query_order_attr = "d.title"
        elif order_attr == "source":
            query_order_attr = "d.source"

        # Check order direction
        if order_dir == "desc":
            query_order_dir = "DESC"
        elif order_dir == "asc":
            query_order_dir = "ASC"

        # Check limit parameter
        if limit > 0:
            query_limit = limit

        # Check offset parameter
        if offset > 0:
            query_offset = offset

        # If no profile_ids and field_ids have been passed, i need to return everything
        # && use query without AND xx IN ()
        query = ""
        if len(profile_ids) > 0 and len(field_ids) > 0:
            query = self._query_documents_by_profile_ids_and_field_ids[0]
            query = re.sub(':profile_ids', profile_ids_string, query)
            query = re.sub(':field_ids', field_ids_string, query)
        elif len(profile_ids) > 0 and len(field_ids) == 0:
            query = self._query_documents_by_profile_ids[0]
            query = re.sub(':profile_ids', profile_ids_string, query)
        elif len(profile_ids) == 0 and len(field_ids) > 0:
            query = self._query_documents_by_field_ids[0]
            query = re.sub(':field_ids', field_ids_string, query)
        else:
            query = self._query_all_documents[0]

        if only_count:
            select = "SELECT COUNT(DISTINCT cd.id) AS cnt FROM"
            query = re.sub(query_head, select, query)
            query = re.sub('ORDER BY :order_by', '', query)
            query = re.sub('LIMIT :query_limit', '',  query)
        else:
            select = str(
                "DISTINCT "
                "cd.id             AS id,"
                "d.mendeley_id     AS mendeley_id,"
                "d.title           AS title,"
                "d.doc_type        AS doc_type,"
                "d.last_modified   AS last_modified,"
                "d.abstract        AS abstract,"
                "d.source          AS source,"
                "d.pub_year        AS pub_year,"
                "d.authors         AS authors,"
                "d.keywords        AS keywords,"
                "d.tags            AS tags,"
                "d.derived_bibtex  AS derived_bibtex")
            query = re.sub(':select_attributes', select, query)

            # Substitute order_by and query_limit as well
            query = re.sub(':order_by', '{order_attr} {order_dir}'.format(
                order_attr=query_order_attr,
                order_dir=query_order_dir
            ), query)
            query = re.sub(':query_limit', '{offset},{limit}'.format(
                offset=query_offset,
                limit=query_limit
            ), query)

        log.info("Querying documents by profile_ids and field_ids\n"
                 "\t| profile_ids: {profile_ids}\n"
                 "\t| field_ids: {field_ids}\n"
                 "\t| order_attr: {order_attr}\n"
                 "\t| order_dir: {order_dir}\n"
                 "\t| offset: {offset}\n"
                 "\t| limit: {limit}\n"
                 "\t| only_count: {only_count}".format(
            profile_ids=profile_ids_string,
            field_ids=field_ids_string,
            order_attr=query_order_attr,
            order_dir=query_order_dir,
            offset=query_offset,
            limit=query_limit,
            only_count=only_count
        ))
        log.debug("Query: {query}".format(query=query))

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

    def profile_exists(self, first_name: str, last_name: str):
        """
        Given a firstname and a lastname, return if there is a profile in the database
        :return:
        """
        query = self._query_profile[0]
        query = re.sub(':firstname',  "'%s'" % first_name, query)
        query = re.sub(':lastname', "'%s'" % last_name, query)

        log.info("Querying profile by first_name and last_name\n"
                 "\t| first_name: {first_name}\n"
                 "\t| last_name: {last_name}\n".format(
            first_name=first_name,
            last_name=last_name
        ))

        with self._engine.begin() as conn:
            p = conn.execute(query).fetchone()
            return p is not None


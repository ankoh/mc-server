__author__ = 'kohn'

from sqlalchemy.engine import Engine
from sqlalchemy.sql import text

import textwrap


class ApiScripts:
    def __init__(self, engine: Engine):
        self._engine = engine

    def get_documents_by_profile_ids_and_field_ids(self, profile_ids: [int], field_ids: [int]):
        """
        Given profile ids and field ids, queries all documents that belong to the research field
        AND are associated with these profiles
        :return:
        """
        query = text(
            "SELECT "
            "   d.id, "
            "   d.title "
            "FROM "
            "   mendeley_document md, "
            "   cache_document d, "
            "   cache_profile p, "
            "   cache_field f, "
            "   cache_document_has_cache_field dhf, "
            "   cache_profile_has_cache_document phd "
            "WHERE md.cache_document_id = d.id "
            "AND d.id = dhf.cache_document_id "
            "AND dhf.cache_field_id = f.id "
            "AND d.id = phd.cache_document_id "
            "AND phd.cache_profile_id = p.id "
            "AND f.id in :field_ids "
            "AND p.id in :profile_ids ")
        return self._engine.execute(query, field_ids=field_ids, profile_ids=profile_ids).fetchall()

    def get_slim_profiles(self):
        """
        Query slim profiles for fast UI autocompletion
        :param profile_ids:
        :return:
        """
        query = text(
            "SELECT "
            "   p.id, "
            "   p.name, "
            "   c.cnt "
            "FROM "
            "   cache_profile p,"
            "   ( "
            "     SELECT p.id as id, count(*) as cnt"
            "     FROM "
            "      cache_profile p, "
            "      cache_document d, "
            "      cache_profile_has_cache_document phd "
            "     WHERE p.id = phd.cache_profile_id "
            "     AND d.id = phd.cache_document_id "
            "     GROUP BY p.id "
            "   ) c "
            "WHERE p.id = c.id"
        )
        return self._engine.execute(query).fetchall()

    def get_profiles_by_profile_ids_or_field_ids(self, profile_ids: [int], field_ids: [int]):
        """
        Given a list of profile ids and field ids, queries all profiles that belong to the research field
        OR are associated with the profile_ids.
        :param slim:
        :return:
        """
        query = text(
            "SELECT "
            "   mp, "
            "   c.cnt "
            "FROM "
            "   cache_profile p, "
            "   mendeley_profile mp, "
            "   ( "
            "     SELECT id, MAX(cnt) as cnt"
            "     FROM "
            "     ( "
            "       ( "
            "        SELECT p.id as id , count(*) as cnt "
            "        FROM "
            "           cache_profile p,"
            "           cache_document d, "
            "           cache_profile_has_cache_document phd "
            "        WHERE p.id = phd.cache_profile_id "
            "        AND phd.cache_document_id = d.id "
            "        AND p.id IN :profile_ids "
            "        GROUP BY p.id "
            "       ) "
            "       UNION ALL "
            "       ( "
            "        SELECT p.id as id, count(*) as cnt "
            "         FROM "
            "           cache_profile p, "
            "           cache_document d, "
            "           cache_field f, "
            "           cache_profile_has_cache_document phd, "
            "           cache_document_has_cache_field dhf "
            "        WHERE p.id = phd.cache_profile_id "
            "        AND phd.cache_document_id = d.id "
            "        AND d.id = dhf.cache_document_id "
            "        AND dhf.cache_field_id = f.id "
            "        AND f.id IN :field_ids "
            "        GROUP BY p.id "
            "       ) "
            "     ) "
            "     GROUP BY id "
            "   ) c "
            "WHERE p.id = c.id "
            "AND p.id = mp.cache_profile_id "
        )
        return self._engine.execute(query, field_ids=field_ids, profile_ids=profile_ids).fetchall()

    def get_fields(self):
        """
        Queries all research fields
        :return:
        """
        query = text(
            "SELECT "
            "   f.id, "
            "   f.title, "
            "   c.cnt "
            "FROM "
            "   cache_field f, "
            "   ( "
            "      SELECT f.id as id, count(*) as cnt "
            "      FROM "
            "        cache_field f, "
            "        cache_document d, "
            "        cache_document_has_cache_field dhf "
            "      WHERE f.id = dhf.cache_document_id "
            "      AND dhf.cache_document_id = d.id "
            "      GROUP BY f.id "
            "   ) c "
            "WHERE f.id = c.id "
        )
        return self._engine.execute(query).fetchall()


    def get_general_statistics(self):
        """
        Queries the access logs to get the statistics of the past seven weeks (grouped by week)
        :return:
        """
        pass

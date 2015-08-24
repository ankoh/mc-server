__author__ = 'kohn'

from mendeleycache.utils.files import get_relative_path
from mendeleycache.utils.regex import sql_comments
from mendeleycache.analyzer.unification import unify_document_title
from mendeleycache.models import Document, Profile
from sqlalchemy.engine import Engine

import re


class CrawlScripts:
    def __init__(self, engine: Engine):
        self._engine = engine

        self._replace_mendeley_documents = ""
        self._replace_mendeley_profiles = ""
        self._update_cache_documents = ""
        self._update_cache_fields = ""
        self._update_cache_profiles = ""
        self._link_fields_to_documents = ""
        self._link_profiles_to_documents = ""

        self.read_sql()

    def read_sql(self):
        """
        Read the sql files and load them into the class variables
        :return:
        """
        path = get_relative_path('sql', 'crawler', 'replace_mendeley_documents.sql')
        with open(path, "r") as sql_file:
            sql = sql_file.read()
            self._replace_mendeley_documents = re.sub(sql_comments, ' ', sql).replace('\n', ' ')

        path = get_relative_path('sql', 'crawler', 'replace_mendeley_profiles.sql')
        with open(path, "r") as sql_file:
            sql = sql_file.read()
            self._replace_mendeley_profiles = re.sub(sql_comments, ' ', sql).replace('\n', ' ')

        path = get_relative_path('sql', 'crawler', 'update_cache_documents.sql')
        with open(path, "r") as sql_file:
            sql = sql_file.read()
            self._update_cache_documents = re.sub(sql_comments, ' ', sql).replace('\n', ' ')

        path = get_relative_path('sql', 'crawler', 'update_cache_fields.sql')
        with open(path, "r") as sql_file:
            sql = sql_file.read()
            self._update_cache_fields = re.sub(sql_comments, ' ', sql).replace('\n', ' ')

        path = get_relative_path('sql', 'crawler', 'update_cache_profiles.sql')
        with open(path, "r") as sql_file:
            sql = sql_file.read()
            self._update_cache_profiles = re.sub(sql_comments, ' ', sql).replace('\n', ' ')

        path = get_relative_path('sql', 'crawler', 'link_fields_to_documents.sql')
        with open(path, "r") as sql_file:
            sql = sql_file.read()
            self._link_fields_to_documents = re.sub(sql_comments, ' ', sql).replace('\n', ' ')

        path = get_relative_path('sql', 'crawler', 'link_profiles_to_documents.sql')
        with open(path, "r") as sql_file:
            sql = sql_file.read()
            self._link_profiles_to_documents = re.sub(sql_comments, ' ', sql).replace('\n', ' ')

    def replace_mendeley_documents(self, docs: [Document]):
        """
        Given a document list, this method replaces the documents in the database with new ones
        :param docs:
        :return:
        """

        def prepare_doc(doc: Document) -> str:
            r = "({unified_title}," \
                "{m_core_id}," \
                "{m_core_profile_id}," \
                "{m_core_title}," \
                "{m_core_type}," \
                "{m_core_created}," \
                "{m_core_last_modified}," \
                "{m_core_abstract}," \
                "{m_core_source}," \
                "{m_core_year}," \
                "{m_core_authors}," \
                "{m_core_keywords}," \
                "{m_tags_tags}," \
                "{derived_bibtex})"
            u, _ = unify_document_title(doc.core_title)
            r.format(
                unified_title=u,
                m_core_id=doc.core_id,
                m_core_profile_id = doc.core_profile_id,
                m_core_title = doc.core_title,
                m_core_type = doc.core_type,
                m_core_created = doc.core_created,
                m_core_last_modified = doc.core_last_modified,
                m_core_abstract = doc.core_abstract,
                m_core_source = doc.core_source,
                m_core_year = doc.core_year,
                m_core_authors = "",
                m_core_keywords = "",
                m_tags_tags = "",
                derived_bibtex = "")
            return r

        mendeley_documents_string = "(%s)" % (",".join(map(prepare_doc, docs)))
        sql = self._replace_mendeley_documents
        sql = re.sub(':mendeley_documents', mendeley_documents_string, sql)
        return self._engine.execute(sql).fetchall()

    
    
    def replace_mendeley_profiles(self,
                                  docs: [Profile]):
        """
        Given a profile list, this method replaces the profiles in the database with new ones
        :param docs:
        :return:
        """
        sql = self._replace_mendeley_profiles

        return self._engine.execute(sql).fetchall()
    
    
    def update_cache_documents(self,
                               unified_document_title_to_documents: {}):
        """
        Given a unified_document_title to documents map, merges the documents and creates the FK references
        :param unified_document_title_to_documents:
        :return:
        """
        sql = self._update_cache_documents

        return self._engine.execute(sql).fetchall()
    
    
    def update_cache_profiles(self,
                              unified_name_to_profiles: {},
                              unified_name_to_real_name: {}):
        """
        Given a unified_profile_name to profiles map, merges the profiles and creates the FK references
        :param unified_name_to_profiles:
        :param unified_name_to_real_name:
        :return:
        """
        sql = self._update_cache_profiles

        return self._engine.execute(sql).fetchall()

    
    def update_cache_fields(self,
                            unified_field_title_to_field: {}):
        """
        Given a unified_field_title to field map, updates the fields
        :param unified_field_title_to_field:
        :return:
        """
        sql = self._update_cache_fields

        return self._engine.execute(sql).fetchall()
    
    
    def link_profiles_to_documents(self,
                                   unified_name_to_authored_documents: {},
                                   unified_name_to_participated_documents: {}):
        """
        Given a unified_profile_name to authored_documents and participated_documents map(s), creates the N:M relations
        in the database
        :param unified_name_to_authored_documents:
        :param unified_name_to_participated_documents:
        :return:
        """
        sql = self._link_profiles_to_documents

        return self._engine.execute(sql).fetchall()
    
    
    def link_fields_to_documents(self,
                                 unified_field_title_to_documents: {}):
        """
        Given a unified_field_title to documents map, creates the N:M relations in the database
        :param unified_field_title_to_documents:
        :return:
        """
        sql = self._link_fields_to_documents

        return self._engine.execute(sql).fetchall()

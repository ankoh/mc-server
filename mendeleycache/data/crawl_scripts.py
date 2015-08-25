__author__ = 'kohn'

from mendeleycache.data.reader import read_single_statement_sql_file
from mendeleycache.analyzer.unification import unify_document_title, unify_profile_name
from mendeleycache.models import Document, Profile
from sqlalchemy.engine import Engine

import re


class CrawlScripts:
    def __init__(self, engine: Engine):
        self._engine = engine

        self._replace_mendeley_documents =\
            read_single_statement_sql_file('sql', 'crawler', 'replace_mendeley_documents.sql')
        self._replace_mendeley_profiles = \
            read_single_statement_sql_file('sql', 'crawler', 'replace_mendeley_profiles.sql')
        self._update_cache_documents = \
            read_single_statement_sql_file('sql', 'crawler', 'update_cache_documents.sql')
        self._update_cache_fields = \
            read_single_statement_sql_file('sql', 'crawler', 'update_cache_fields.sql')
        self._update_cache_profiles = \
            read_single_statement_sql_file('sql', 'crawler', 'update_cache_profiles.sql')
        self._link_fields_to_documents = \
            read_single_statement_sql_file('sql', 'crawler', 'link_fields_to_documents.sql')
        self._link_profiles_to_documents = \
            read_single_statement_sql_file('sql', 'crawler', 'link_profiles_to_documents.sql')

    def replace_mendeley_documents(self, docs: [Document]):
        """
        Given a document list, this method replaces the documents in the database with new ones
        :param docs:
        :return:
        """

        def prepare_doc(doc: Document) -> str:
            r = "({mid}," \
                "{owner_mid}," \
                "{unified_title}," \
                "{title}," \
                "{type}," \
                "{created}," \
                "{last_modified}," \
                "{abstract}," \
                "{source}," \
                "{year}," \
                "{authors}," \
                "{keywords}," \
                "{tags}," \
                "{derived_bibtex})"
            u, _ = unify_document_title(doc.core_title)
            return r.format(
                mid=doc.core_id,
                owner_mid=doc.core_profile_id,
                unified_title=u,
                title=doc.core_title,
                type=doc.core_type,
                created=doc.core_created,
                last_modified=doc.core_last_modified,
                abstract=doc.core_abstract,
                source=doc.core_source,
                year=doc.core_year,
                authors="",
                keywords="",
                tags=""
            )

        mendeley_documents_string = "(%s)" % (",".join(map(prepare_doc, docs)))
        sql = self._replace_mendeley_documents
        sql = re.sub(':documents', mendeley_documents_string, sql)
        return self._engine.execute(sql).fetchall()

    def replace_mendeley_profiles(self,
                                  profiles: [Profile]):
        """
        Given a profile list, this method replaces the profiles in the database with new ones
        :param docs:
        :return:
        """

        def prepare_profile(p: Profile) -> str:
            r = "({mid}," \
                "{unified_name}," \
                "{first_name}," \
                "{last_name}," \
                "{display_name}," \
                "{link})"
            u, _ = unify_profile_name(p.first_name, p.last_name)
            return r.format(
                mid=p.identifier,
                unified_name=u,
                first_name=p.first_name,
                last_name=p.last_name,
                display_name=p.display_name,
                link=p.link
            )

        mendeley_profiles_string = "(%s)" % (",".join(map(prepare_profile, profiles)))
        sql = self._replace_mendeley_documents
        sql = re.sub(':profiles', mendeley_profiles_string, sql)
        return self._engine.execute(sql).fetchall()

    def update_cache_documents(self,
                               unified_document_title_to_documents: {}):
        """
        Given a unified_document_title to documents map, merges the documents and creates the FK references
        :param unified_document_title_to_documents:
        :return:
        """
        cache_document_strings = []
        for unified_title, doc_list in unified_document_title_to_documents.iteritems():
            # flatten the document list down to one document
            reference_doc = None
            """:type : Document"""

            for doc in doc_list:
                if reference_doc is None or doc.core_last_modified > reference_doc.core_last_modified:
                    reference_doc = doc

            # if we found at least one reference_doc (which we will always),
            # add the corresponding sql insert string to the r array
            if reference_doc is not None:
                u, r = unify_document_title(reference_doc.core_title)
                s = "({document_mid}," \
                    "{unified_title}," \
                    "{title})"
                cache_document_strings.append(
                    s.format(
                        document_mid=reference_doc.core_id,
                        unified_title=u,
                        title=r
                    )
                )
        cache_documents_string = '(%s)' % (','.join(cache_document_strings))
        sql = self._update_cache_documents
        sql = re.sub(':cache_documents', cache_documents_string, sql)
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

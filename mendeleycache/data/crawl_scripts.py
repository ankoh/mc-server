__author__ = 'kohn'

from mendeleycache.data.reader import read_single_statement_sql_file
from mendeleycache.analyzer.unification import *
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

    def replace_documents(self, docs: [Document]):
        """
        Given a document list, this method replaces the documents in the database with new ones
        :param docs:
        :return:
        """

        def prepare_doc(doc: Document) -> str:
            r = "('{mid}'," \
                "'{owner_mid}'," \
                "'{unified_title}'," \
                "'{title}'," \
                "'{type}'," \
                "'{created}'," \
                "'{last_modified}'," \
                "'{abstract}'," \
                "'{source}'," \
                "'{year}'," \
                "'{authors}'," \
                "'{keywords}'," \
                "'{tags}'," \
                "'{derived_bibtex}')"
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

        # If there's nothing to insert, abort
        if len(docs) == 0:
            return None

        documents_string = ",".join(map(prepare_doc, docs))
        sql = self._replace_mendeley_documents
        sql = re.sub(':documents', documents_string, sql)
        
        # Fire the sql script in a transaction
        with self._engine.begin() as conn:
            return self._engine.execute(sql).fetchall()

    def replace_profiles(self, profiles: [Profile]):
        """
        Given a profile list, this method replaces the profiles in the database with new ones
        :param docs:
        :return:
        """

        def prepare_profile(p: Profile) -> str:
            r = "('{mid}'," \
                "'{unified_name}'," \
                "'{first_name}'," \
                "'{last_name}'," \
                "'{display_name}'," \
                "'{link}')"
            u, _ = unify_profile_name(p.first_name, p.last_name)
            return r.format(
                mid=p.identifier,
                unified_name=u,
                first_name=p.first_name,
                last_name=p.last_name,
                display_name=p.display_name,
                link=p.link
            )

        # If there's nothing to insert, abort
        if len(profiles) == 0:
            return None

        mendeley_profiles_string = ",".join(map(prepare_profile, profiles))
        sql = self._replace_mendeley_profiles
        sql = re.sub(':profiles', mendeley_profiles_string, sql)

        # Fire the sql script in a transaction
        with self._engine.begin() as conn:
            return self._engine.execute(sql)

    def update_cache_documents(self,
                               unified_document_title_to_documents: {}):
        """
        Given a unified_document_title to documents map, merges the documents and creates the FK references
        :param unified_document_title_to_documents:
        :return:
        """
        cache_document_strings = []
        for _, doc_list in unified_document_title_to_documents.items():
            # flatten the document list down to one document
            reference_doc = None
            """:type : Document"""

            for doc in doc_list:
                if reference_doc is None or doc.core_last_modified > reference_doc.core_last_modified:
                    reference_doc = doc

            # if we found at least one reference_doc (which we should),
            # add the corresponding sql insert string to the cache_document_strings array
            if reference_doc is not None:
                u, r = unify_document_title(reference_doc.core_title)
                s = "('{document_mid}'," \
                    "'{unified_title}'," \
                    "'{title}')"
                cache_document_strings.append(
                    s.format(
                        document_mid=reference_doc.core_id,
                        unified_title=u,
                        title=r
                    )
                )

        # If there's nothing to insert, abort
        if len(cache_document_strings) == 0:
            return None

        cache_documents_string = ','.join(cache_document_strings)
        sql = self._update_cache_documents
        sql = re.sub(':cache_documents', cache_documents_string, sql)
        return self._engine.execute(sql).fetchall()

    def update_cache_profiles(self,
                              unified_name_to_profiles: {}):
        """
        Given a unified_profile_name to profiles map, merges the profiles and creates the FK references
        :param unified_name_to_profiles:
        :param unified_name_to_real_name:
        :return:
        """
        cache_profile_strings = []
        for _, profile_list in unified_name_to_profiles.items():
            # flatten the profile list down to one profile
            reference_profile = None
            """:type : Profile"""

            for profile in profile_list:
                if reference_profile is None or len(profile.display_name) > len(reference_profile.display_name):
                    reference_profile = profile

            # if we found at least one reference_profile (which we should)
            # add the corresponding sql insert string to the cache_profile_strings array
            if reference_profile is not None:
                u, r = unify_profile_name(profile.first_name, profile.last_name)
                s = "('{profile_mid}'," \
                    "'{unified_title}'," \
                    "'{title}')"
                cache_profile_strings.append(
                    s.format(
                        profile_mid=reference_profile.identifier,
                        unified_name=u,
                        name=r
                    )
                )

        # If there's nothing to insert, abort
        if len(cache_profile_strings) == 0:
            return None

        cache_profiles_string = ','.join(cache_profile_strings)
        sql = self._update_cache_profiles
        sql = re.sub(':cache_profiles', cache_profiles_string, sql)
        return self._engine.execute(sql).fetchall()

    def update_cache_fields(self,
                            unified_field_title_to_field: {}):
        """
        Given a unified_field_title to field map, updates the fields
        :param unified_field_title_to_field:
        :return:
        """
        cache_field_strings = []
        for _, field in unified_field_title_to_field.items():
            s = "('{unified_title}','{title}')"
            cache_field_strings.append(
                s.format(
                    unified_title=field.unified_title,
                    title=field.title
                )
            )

        # If there's nothing to insert, abort
        if len(cache_field_strings) == 0:
            return None

        cache_fields_string = ','.join(cache_field_strings)
        sql = self._update_cache_fields
        sql = re.sub(':cache_fields', cache_fields_string, sql)
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
        unified_name_unified_title_tuple_strings=[]
        for unified_name, doc_list in unified_name_to_authored_documents:
            for doc_unified in doc_list:
                s = "('{unified_name}','{unified_title}')"
                unified_name_unified_title_tuple_strings.append(
                    s.format(
                        unified_name=unified_name,
                        unified_title=doc_unified
                    )
                )

        for unified_name, doc_list in unified_name_to_participated_documents:
            for doc_unified in doc_list:
                s = "('{unified_name}','{unified_title}')"
                unified_name_unified_title_tuple_strings.append(
                    s.format(
                        unified_name=unified_name,
                        unified_title=doc_unified
                    )
                )

        # If there's nothing to insert, abort
        if len(unified_name_unified_title_tuple_strings) == 0:
            return None

        unified_name_unified_title_tuples_string = ','.join(unified_name_unified_title_tuple_strings)
        sql = self._link_profiles_to_documents
        sql = re.sub(':profile_has_document', unified_name_unified_title_tuples_string, sql)
        return self._engine.execute(sql).fetchall()

    def link_fields_to_documents(self,
                                 unified_field_title_to_documents: {}):
        """
        Given a unified_field_title to documents map, creates the N:M relations in the database
        :param unified_field_title_to_documents:
        :return:
        """
        field_title_doc_title_tuple_strings=[]
        for unified_field_title, doc_list in unified_field_title_to_documents:
            for doc_unified in doc_list:
                s = "('{unified_field_title}','{unified_doc_title}')"
                field_title_doc_title_tuple_strings.append(
                    s.format(
                        unified_field_title=unified_field_title,
                        unified_doc_title=doc_unified
                    )
                )

        # If there's nothing to insert, abort
        if len(field_title_doc_title_tuple_strings) == 0:
            return None

        field_title_doc_title_tuples_string = ','.join(field_title_doc_title_tuple_strings)
        sql = self._link_fields_to_documents
        sql = re.sub(':document_has_field', field_title_doc_title_tuples_string, sql)
        return self._engine.execute(sql).fetchall()

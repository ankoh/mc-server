__author__ = 'kohn'

from mendeleycache.data.reader import read_sql_statements
from mendeleycache.analyzer.unification import *
from mendeleycache.models import Document, Profile
from mendeleycache.utils.sanitize import sanitize_text
from sqlalchemy.engine import Engine

import re


class CrawlData:
    def __init__(self, engine: Engine):
        self._engine = engine

        self._replace_documents =\
            read_sql_statements('sql', 'crawler', 'update_documents.sql')
        self._replace_profiles = \
            read_sql_statements('sql', 'crawler', 'update_profiles.sql')
        self._update_cache_documents = \
            read_sql_statements('sql', 'crawler', 'update_cache_documents.sql')
        self._update_cache_fields = \
            read_sql_statements('sql', 'crawler', 'update_cache_fields.sql')
        self._update_cache_profiles = \
            read_sql_statements('sql', 'crawler', 'update_cache_profiles.sql')
        self._link_fields_to_documents = \
            read_sql_statements('sql', 'crawler', 'link_fields_to_documents.sql')
        self._link_profiles_to_documents = \
            read_sql_statements('sql', 'crawler', 'link_profiles_to_documents.sql')
        self._generate_cache_links = \
            read_sql_statements('sql', 'crawler', 'generate_cache_links.sql')

    def update_documents(self, docs: [Document]):
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
                "'{doc_type}'," \
                "'{created}'," \
                "'{last_modified}'," \
                "'{abstract}'," \
                "'{source}'," \
                "'{pub_year}'," \
                "'{authors}'," \
                "'{keywords}'," \
                "'{tags}'," \
                "'{derived_bibtex}')"
            u, _ = unify_document_title(doc.core_title)
            return r.format(
                mid=sanitize_text(doc.core_id),
                owner_mid=sanitize_text(doc.core_profile_id),
                unified_title=sanitize_text(u),
                title=sanitize_text(doc.core_title),
                doc_type=sanitize_text(doc.core_type),
                created=doc.core_created,
                last_modified=doc.core_last_modified,
                abstract=sanitize_text(doc.core_abstract),
                source=sanitize_text(doc.core_source),
                pub_year=doc.core_year,
                authors="",
                keywords="",
                tags="",
                derived_bibtex=""
            )

        # If there's nothing to insert, abort
        if len(docs) == 0:
            return None

        delete = self._replace_documents[0]
        insert = self._replace_documents[1]

        documents_string = ",".join(map(prepare_doc, docs))
        insert = re.sub(':documents', documents_string, insert)
        
        # Fire the sql script in a transaction
        with self._engine.begin() as conn:
            conn.execute(delete)
            return conn.execute(insert)

    def update_profiles(self, profiles: [Profile]):
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
                mid=sanitize_text(p.identifier),
                unified_name=sanitize_text(u),
                first_name=sanitize_text(p.first_name),
                last_name=sanitize_text(p.last_name),
                display_name=sanitize_text(p.display_name),
                link=sanitize_text(p.link)
            )

        # If there's nothing to insert, abort
        if len(profiles) == 0:
            return None

        delete = self._replace_profiles[0]
        insert = self._replace_profiles[1]

        mendeley_profiles_string = ",".join(map(prepare_profile, profiles))
        insert = re.sub(':profiles', mendeley_profiles_string, insert)

        # Fire the sql script in a transaction
        with self._engine.begin() as conn:
            conn.execute(delete)
            return conn.execute(insert)

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
                        document_mid=sanitize_text(reference_doc.core_id),
                        unified_title=sanitize_text(u),
                        title=sanitize_text(r)
                    )
                )

        # If there's nothing to insert, abort
        if len(cache_document_strings) == 0:
            return None

        cache_documents_string = ','.join(cache_document_strings)
        sql = self._update_cache_documents[0]
        sql = re.sub(':cache_documents', cache_documents_string, sql)

        # Fire the sql script in a transaction
        with self._engine.begin() as conn:
            return conn.execute(sql)

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
                    "'{unified_name}'," \
                    "'{name}')"
                cache_profile_strings.append(
                    s.format(
                        profile_mid=sanitize_text(reference_profile.identifier),
                        unified_name=sanitize_text(u),
                        name=sanitize_text(r)
                    )
                )

        # If there's nothing to insert, abort
        if len(cache_profile_strings) == 0:
            return None

        cache_profiles_string = ','.join(cache_profile_strings)
        sql = self._update_cache_profiles[0]
        sql = re.sub(':cache_profiles', cache_profiles_string, sql)

        # Fire the sql script in a transaction
        with self._engine.begin() as conn:
            return conn.execute(sql)

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
                    unified_title=sanitize_text(field.unified_title),
                    title=sanitize_text(field.title)
                )
            )

        # If there's nothing to insert, abort
        if len(cache_field_strings) == 0:
            return None

        cache_fields_string = ','.join(cache_field_strings)
        sql = self._update_cache_fields[0]
        sql = re.sub(':cache_fields', cache_fields_string, sql)

        # Fire the sql script in a transaction
        with self._engine.begin() as conn:
            return conn.execute(sql)
    
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
        for unified_name, doc_list in unified_name_to_authored_documents.items():
            for doc_unified in doc_list:
                s = "('{unified_name}','{unified_title}')"
                unified_name_unified_title_tuple_strings.append(
                    s.format(
                        unified_name=sanitize_text(unified_name),
                        unified_title=sanitize_text(doc_unified)
                    )
                )

        for unified_name, doc_list in unified_name_to_participated_documents.items():
            for doc_unified in doc_list:
                s = "('{unified_name}','{unified_title}')"
                unified_name_unified_title_tuple_strings.append(
                    s.format(
                        unified_name=sanitize_text(unified_name),
                        unified_title=sanitize_text(doc_unified)
                    )
                )

        # If there's nothing to insert, abort
        if len(unified_name_unified_title_tuple_strings) == 0:
            return None

        # Get the different statements in the sql file
        temp = self._link_profiles_to_documents[0]
        insert = self._link_profiles_to_documents[1]
        delete = self._link_profiles_to_documents[2]
        link = self._link_profiles_to_documents[3]
        drop = self._link_profiles_to_documents[4]

        unified_name_unified_title_tuples_string = '%s' % ','.join(unified_name_unified_title_tuple_strings)
        insert = re.sub(':profiles_to_documents', unified_name_unified_title_tuples_string, insert)



        # Fire the sql scripts in a transaction
        with self._engine.begin() as conn:
            conn.execute(temp)
            conn.execute(insert)
            conn.execute(delete)
            conn.execute(link)
            conn.execute(drop)

    def link_fields_to_documents(self,
                                 unified_field_title_to_documents: {}):
        """
        Given a unified_field_title to documents map, creates the N:M relations in the database
        :param unified_field_title_to_documents:
        :return:
        """
        field_title_doc_title_tuple_strings=[]
        for unified_field_title, doc_list in unified_field_title_to_documents.items():
            for doc_unified in doc_list:
                s = "('{unified_field_title}','{unified_doc_title}')"
                field_title_doc_title_tuple_strings.append(
                    s.format(
                        unified_field_title=sanitize_text(unified_field_title),
                        unified_doc_title=sanitize_text(doc_unified)
                    )
                )

        # If there's nothing to insert, abort
        if len(field_title_doc_title_tuple_strings) == 0:
            return None

         # Get the different statements in the sql file
        temp = self._link_profiles_to_documents[0]
        insert = self._link_profiles_to_documents[1]
        delete = self._link_profiles_to_documents[2]
        link = self._link_profiles_to_documents[3]
        drop = self._link_profiles_to_documents[4]

        field_title_doc_title_tuples_string = '%s' % ','.join(field_title_doc_title_tuple_strings)
        insert = re.sub(':fields_to_documents', field_title_doc_title_tuples_string, insert)

        # Fire the sql scripts in a transaction
        with self._engine.begin() as conn:
            conn.execute(temp)
            conn.execute(insert)
            conn.execute(delete)
            conn.execute(link)
            conn.execute(drop)

    def generate_cache_links(self):
        """
        Executes all linking steps that are required for the queries
        :return:
        """
        with self._engine.begin() as conn:
            for stmt in self._generate_cache_links:
                conn.execute(stmt)

    def execute(self,
                profiles,
                documents,
                unified_name_to_profiles,
                unified_document_title_to_documents,
                unified_field_title_to_field,
                unified_name_to_authored_documents,
                unified_name_to_participated_documents):
        """
        Given the required crawl data updates the whole cache
        :return:
        """
        self.update_profiles(profiles)
        self.update_documents(documents)
        self.update_cache_profiles(unified_name_to_profiles)
        self.update_cache_documents(unified_document_title_to_documents)
        self.update_cache_fields(unified_field_title_to_field)
        self.link_profiles_to_documents(
            unified_name_to_authored_documents,
            unified_name_to_participated_documents
        )
        self.generate_cache_links()

__author__ = 'kohn'

from mendeleycache.data.reader import read_sql_statements
from mendeleycache.data.identifiers import generate_id
from mendeleycache.data.bibtex import generate_bibtex
from mendeleycache.analyzer.unification import *
from mendeleycache.models import Document, Profile
from mendeleycache.utils.sanitize import sanitize_text
from sqlalchemy.engine import Engine

import re
import functools


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
        self._post_update = \
            read_sql_statements('sql', 'crawler', 'post_update.sql')

    def update_documents(self, docs: [Document]):
        """
        Given a document list, this method replaces the documents in the database with new ones
        :param docs:
        :return:
        """

        def prepare_doc(doc: Document) -> str:
            r = "('{mendeley_id}'," \
                "'{cache_document_id}'," \
                "'{owner_mendeley_id}'," \
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
            b64u = generate_id(u)

            # Produce plain TEXT from the lists
            author_string = map(lambda x: "{first} {last}".format(first=x[0], last=x[1]), doc.core_authors)
            authors_string = ", ".join(author_string)
            keywords_string = ", ".join(doc.core_keywords)
            tags_string = ", ".join(doc.tags)

            # Generate bibtex
            bibtex = generate_bibtex(doc)

            return r.format(
                mendeley_id=sanitize_text(doc.core_id),
                cache_document_id=b64u,
                owner_mendeley_id=sanitize_text(doc.core_profile_id),
                title=sanitize_text(doc.core_title),
                doc_type=sanitize_text(doc.core_type),
                created=doc.core_created,
                last_modified=doc.core_last_modified,
                abstract=sanitize_text(doc.core_abstract),
                source=sanitize_text(doc.core_source),
                pub_year=doc.core_year,
                authors=authors_string,
                keywords=keywords_string,
                tags=tags_string,
                derived_bibtex=bibtex
            )

        # If there's nothing to insert, abort
        if len(docs) == 0:
            return None

        delete = self._replace_documents[0]
        insert = self._replace_documents[1]
        temp = self._replace_documents[2]
        temp_insert = self._replace_documents[3]
        update = self._replace_documents[4]
        temp_drop = self._replace_documents[5]

        documents_string = ",".join(map(prepare_doc, docs))
        insert = re.sub(':documents', documents_string, insert)
        
        # Fire the sql script in a transaction
        with self._engine.begin() as conn:
            conn.execute(delete)
            conn.execute(insert)
            conn.execute(temp)
            conn.execute(temp_insert)
            conn.execute(update)
            conn.execute(temp_drop)

    def update_profiles(self, profiles: [Profile]):
        """
        Given a profile list, this method replaces the profiles in the database with new ones
        :param docs:
        :return:
        """

        def prepare_profile(p: Profile) -> str:
            r = "('{mendeley_id}'," \
                "'{cache_profile_id}'," \
                "'{first_name}'," \
                "'{last_name}'," \
                "'{display_name}'," \
                "'{link}')"
            u, _ = unify_profile_name(p.first_name, p.last_name)
            b64u = generate_id(u)
            return r.format(
                mendeley_id=sanitize_text(p.identifier),
                cache_profile_id=b64u,
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
        temp = self._replace_profiles[2]
        temp_insert = self._replace_profiles[3]
        update = self._replace_profiles[4]
        temp_drop = self._replace_profiles[5]

        mendeley_profiles_string = ",".join(map(prepare_profile, profiles))
        insert = re.sub(':profiles', mendeley_profiles_string, insert)

        # Fire the sql script in a transaction
        with self._engine.begin() as conn:
            conn.execute(delete)
            conn.execute(insert)
            conn.execute(temp)
            conn.execute(temp_insert)
            conn.execute(update)
            conn.execute(temp_drop)

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
                b64u = generate_id(u)
                s = "('{id}','{title}')"
                cache_document_strings.append(
                    s.format(
                        id=b64u,
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
                b64u = generate_id(u)
                s = "('{id}','{name}')"
                cache_profile_strings.append(
                    s.format(
                        id=b64u,
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
            b64u = generate_id(field.unified_title)
            s = "('{id}','{title}')"
            cache_field_strings.append(
                s.format(
                    id=b64u,
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
                s = "('{cache_profile_id}','{cache_document_id}')"
                unified_name_unified_title_tuple_strings.append(
                    s.format(
                        cache_profile_id=generate_id(unified_name),
                        cache_document_id=generate_id(doc_unified)
                    )
                )

        for unified_name, doc_list in unified_name_to_participated_documents.items():
            for doc_unified in doc_list:
                s = "('{cache_profile_id}','{cache_document_id}')"
                unified_name_unified_title_tuple_strings.append(
                    s.format(
                        cache_profile_id=generate_id(unified_name),
                        cache_document_id=generate_id(doc_unified)
                    )
                )

        # If there's nothing to insert, abort
        if len(unified_name_unified_title_tuple_strings) == 0:
            return None

        # Get the different statements in the sql file
        delete = self._link_profiles_to_documents[0]
        insert = self._link_profiles_to_documents[1]

        unified_name_unified_title_tuples_string = '%s' % ','.join(unified_name_unified_title_tuple_strings)
        insert = re.sub(':profiles_to_documents', unified_name_unified_title_tuples_string, insert)

        # Fire the sql scripts in a transaction
        with self._engine.begin() as conn:
            conn.execute(delete)
            conn.execute(insert)

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
                s = "('{cache_document_id}','{cache_field_id}')"
                field_title_doc_title_tuple_strings.append(
                    s.format(
                        cache_document_id=generate_id(unified_field_title),
                        cache_field_id=generate_id(doc_unified)
                    )
                )

        # If there's nothing to insert, abort
        if len(field_title_doc_title_tuple_strings) == 0:
            return None

         # Get the different statements in the sql file
        delete = self._link_fields_to_documents[0]
        insert = self._link_fields_to_documents[1]

        field_title_doc_title_tuples_string = '%s' % ','.join(field_title_doc_title_tuple_strings)
        insert = re.sub(':fields_to_documents', field_title_doc_title_tuples_string, insert)

        # Fire the sql scripts in a transaction
        with self._engine.begin() as conn:
            conn.execute(delete)
            conn.execute(insert)

    def post_update(self):
        """
        Executes all linking steps that are required for the queries
        :return:
        """
        with self._engine.begin() as conn:
            for stmt in self._post_update:
                conn.execute(stmt)

    def execute(self,
                profiles,
                documents,
                unified_name_to_profiles,
                unified_document_title_to_documents,
                unified_field_title_to_field,
                unified_field_title_to_documents,
                unified_name_to_authored_documents,
                unified_name_to_participated_documents):
        """
        Given the required crawl data updates the whole cache
        :return:
        """
        self.update_cache_profiles(unified_name_to_profiles)
        self.update_cache_documents(unified_document_title_to_documents)
        self.update_profiles(profiles)
        self.update_documents(documents)
        self.update_cache_fields(unified_field_title_to_field)
        self.link_profiles_to_documents(
            unified_name_to_authored_documents,
            unified_name_to_participated_documents
        )
        self.link_fields_to_documents(unified_field_title_to_documents)
        self.post_update()

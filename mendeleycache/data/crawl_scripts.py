__author__ = 'kohn'

from mendeleycache.models import Document, Profile
from sqlalchemy.engine import Engine


class CrawlScripts:
    def __init__(self, engine: Engine):
        self._engine = engine

    def replace_mendeley_documents(docs: [Document]):
        """
        Given a document list, this method replaces the documents in the database with new ones
        :param docs:
        :return:
        """
        pass
    
    
    def replace_mendeley_profiles(docs: [Profile]):
        """
        Given a profile list, this method replaces the profiles in the database with new ones
        :param docs:
        :return:
        """
        pass
    
    
    def update_cache_documents(unified_document_title_to_documents: {}):
        """
        Given a unified_document_title to documents map, merges the documents and creates the FK references
        :param unified_document_title_to_documents:
        :return:
        """
        pass
    
    
    def update_cache_profiles(unified_name_to_profiles: {}, unified_name_to_real_name: {}):
        """
        Given a unified_profile_name to profiles map, merges the profiles and creates the FK references
        :param unified_name_to_profiles:
        :param unified_name_to_real_name:
        :return:
        """
        pass
    
    
    def update_cache_fields(unified_field_title_to_field: {}):
        """
        Given a unified_field_title to field map, updates the fields
        :param unified_field_title_to_field:
        :return:
        """
        pass
    
    
    def link_profiles_to_documents(engine: Engine,
                                   unified_name_to_authored_documents: {},
                                   unified_name_to_participated_documents: {}):
        """
        Given a unified_profile_name to authored_documents and participated_documents map(s), creates the N:M relations
        in the database
        :param unified_name_to_authored_documents:
        :param unified_name_to_participated_documents:
        :return:
        """
        pass
    
    
    def link_fields_to_documents(unified_field_title_to_documents: {}):
        """
        Given a unified_field_title to documents map, creates the N:M relations in the database
        :param unified_field_title_to_documents:
        :return:
        """
        pass

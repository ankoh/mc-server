__author__ = 'kohn'

from mendeleycache.crawler.abstract_crawler import AbstractCrawler
from mendeleycache.crawler.json import get_document_from_json, get_profile_from_json, get_member_from_json
from mendeleycache.crawler.mendeley.extensions import ExtendedDocuments
from mendeleycache.config import ServiceConfiguration
from mendeleycache.models import Member, Profile, Document
from mendeleycache.logging import log

from mendeley import Mendeley
from mendeley.session import MendeleySession

from threading import Lock


class SDKCrawler(AbstractCrawler):
    def __init__(self, app_id: str, app_secret: str):
        self._app_id = app_id
        self._app_secret = app_secret
        self._initialized = False
        self._mendeley = Mendeley(app_id, app_secret)

        self._session = None
        """:type : MendeleySession """

    def prepare(self):
        try:
            self._session = self._mendeley.start_client_credentials_flow().authenticate()
            self._initialized = True
        except Exception as e:
            log.critical(e)

    def destroy(self):
        self._initialized = False

    def get_group_members(self, group_id: str) -> [Member]:
        if not self._initialized:
            log.critical("get_group_members has been fired but the SDKCrawler was not initialized")
            return []
        results = []

        members = self._session.group_members(group_id).iter()
        for member in members:
            m = get_member_from_json(member.member_json)
            if m.role != 'follower':
                results.append(m)
        return results

    def get_profile_by_id(self, profile_id: str) -> Profile:
        if not self._initialized:
            log.critical("get_profile_by_id has been fired but the SDKCrawler was not initialized")
            return []

        profile = self._session.profiles.get(profile_id)
        return get_profile_from_json(profile.json)

    def get_documents_by_profile_id(self, profile_id: str) -> [Document]:
        if not self._initialized:
            log.critical("get_documents_by_profile_id has been fired but the SDKCrawler was not initialized")
            return []
        results = []

        """
        Unfortunately the official Mendeley SDK has no support for document queries by non-logged-in profile-ids
        Therefore i'll hack around that and reuse the session object to authenticate my own call.
        Critical SDK class:
        https://github.com/Mendeley/mendeley-python-sdk/blob/master/mendeley/resources/documents.py
        """

        documents = ExtendedDocuments(self._session).iter(view='all', profile_id=profile_id, authored='true')
        for document in documents:
            d = get_document_from_json(document.json)
            results.append(d)
        return results

    def get_documents_by_group_id(self, group_id: str) -> [Document]:
        if not self._initialized:
            log.critical("get_documents_by_group_id has been fired but the SDKCrawler was not initialized")
            return []
        results = []

        documents = self._session.group_documents(group_id).iter(view='all')
        for document in documents:
            d = get_document_from_json(document.json)
            results.append(d)
        return results

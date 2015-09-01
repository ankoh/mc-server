__author__ = 'kohn'

from mendeley.resources import base
from mendeley.response import SessionResponseObject


class ExtendedDocument(SessionResponseObject):
    content_type = 'application/vnd.mendeley-document.1+json'
    @classmethod
    def fields(cls):
        return ['id', 'title', 'type', 'source', 'year', 'identifiers', 'keywords', 'abstract']


class ExtendedDocuments(base.ListResource):
    """
    This class aims to extend mendeley sdk in order to enable
    documents_by_Profile_id queries of users that are not logged in
    ( Similar to the functionality in the web ui )
    """

    _url = '/documents'

    def __init__(self, session):
        self.session = session

    @property
    def _session(self):
        return self.session

    def iter(self, page_size=None, view=None, sort=None, order=None, modified_since=None, deleted_since=None,
             profile_id=None, authored=None):
        return super(ExtendedDocuments, self).iter(page_size,
                                                  view=view,
                                                  sort=sort,
                                                  order=order,
                                                  modified_since=modified_since,
                                                  deleted_since=deleted_since,
                                                  group_id=None,
                                                  profile_id=profile_id,
                                                  authored=authored)

    def _obj_type(self, **kwargs):
        return ExtendedDocument

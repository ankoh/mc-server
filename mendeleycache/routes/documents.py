__author__ = 'kohn'

from flask import Flask, request

from mendeleycache.data.controller import DataController
from mendeleycache.logging import log
import json


class DocumentsController:
    def __init__(self, app: Flask, data_controller: DataController):
        self._app = app
        self._data_controller = data_controller

    def register(self):
        self._app.add_url_rule('/documents/', view_func=self.get_publications)

    def get_publications(self):
        log.info('The route /documents/ has been triggered')

        # Default parameters
        profile_ids = ''
        field_ids = ''
        slim = False

        # Set passed query parameters if existing
        if 'profile-ids' in request.args:
            profile_ids = request.args.getlist('profile-ids')
            log.debug('Query parameter "profile-ids" = %s' % profile_ids)
        if 'field-ids' in request.args:
            field_ids = request.args.getlist('field-ids')
            log.debug('Query parameter "field_ids" = %s' % field_ids)

        # Trigger the respective methods
        documents = self._data_controller.api_data.get_documents_by_profile_ids_and_field_ids(
            profile_ids=profile_ids,
            field_ids=field_ids
        )

        # Serialize documents
        response = []
        for document in documents:
            document_dict = dict(document.items())
            response.append(document_dict)
        return json.dumps(response)

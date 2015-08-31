__author__ = 'kohn'

from flask import Flask, request

from mendeleycache.utils.json_encoder import DefaultEncoder
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
        limit = 0
        offset = 0
        order_dir = ""
        order_attr = ""
        slim = False

        # Set passed query parameters if existing
        if 'profile-ids' in request.args:
            profile_ids = request.args['profile-ids'].split(',')
            log.debug('Query parameter "profile-ids" = %s' % profile_ids)
        if 'field-ids' in request.args:
            field_ids = request.args['field-ids'].split(',')
            log.debug('Query parameter "field-ids" = %s' % field_ids)
        if 'limit' in request.args:
            limit = int(request.args['limit'])
            log.debug('Query parameter "limit" = %s' % limit)
        if 'offset' in request.args:
            offset = int(request.args['offset'])
            log.debug('Query parameter "offset" = %s' % offset)
        if 'order-dir' in request.args:
            order_dir = request.args['order-dir']
            log.debug('Query parameter "order-dir" = %s' % order_dir)
        if 'order-attr' in request.args:
            order_attr = request.args['order-attr']
            log.debug('Query parameter "order-attr" = %s' % order_attr)

        # Trigger the respective methods
        documents = self._data_controller.api_data.get_documents_by_profile_ids_and_field_ids(
            profile_ids=profile_ids,
            field_ids=field_ids,
            order_attr=order_attr,
            order_dir=order_dir,
            offset=offset,
            limit=limit
        )

        # Serialize documents
        response = []
        for document in documents:
            document_dict = dict(document.items())
            response.append(document_dict)
        return json.dumps(response, cls=DefaultEncoder)

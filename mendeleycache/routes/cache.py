__author__ = 'kohn'

from flask import Flask
from mendeleycache.data.controller import DataController

from mendeleycache.config import ServiceConfiguration
from mendeleycache.logging import log
from mendeleycache.utils.remotes import remote_is_online
from mendeleycache.utils.json_encoder import DefaultEncoder

import json


class CacheController:
    def __init__(self, app: Flask, data_controller: DataController, config: ServiceConfiguration):
        self._app = app
        self._data_controller = data_controller
        self._config = config

    def register(self):
        self._app.add_url_rule('/cache/status', methods=['GET'], view_func=self.get_system_status)
        self._app.add_url_rule('/cache/entities', methods=['GET'], view_func=self.get_system_entities)

    def get_system_status(self):
        log.info('The route /cache/status has been triggered')

        api_online = remote_is_online("api.mendeley.com", 443)

        json_result = dict()
        json_result["serverVersion"] = self._config.version
        json_result["mendeleyStatus"] = "Online" if api_online else "Offline"
        json_result["lastUpdate"] = "Never"

        # TODO: Store lastUpdate through database

        return json.dumps(json_result, cls=DefaultEncoder)

    def get_system_entities(self):
        log.info('The route /cache/entities has been triggered')
        json_result = dict()

        entities = self._data_controller.api_data.get_entities()

        # Serialize fields
        response = []
        for entity in entities:
            columns = dict(entity.items())
            response.append(columns)
        return json.dumps(response, cls=DefaultEncoder)

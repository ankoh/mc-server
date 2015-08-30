__author__ = 'kohn'

from flask import Flask
from mendeleycache.data.controller import DataController

from mendeleycache.config import ServiceConfiguration
from mendeleycache.logging import log

import json


class SystemController:
    def __init__(self, app: Flask, data_controller: DataController, config: ServiceConfiguration):
        self._app = app
        self._data_controller = data_controller
        self._config = config

    def register(self):
        self._app.add_url_rule('/system/status', view_func=self.get_system_status)
        self._app.add_url_rule('/system/entities', view_func=self.get_system_entities)

    def get_system_status(self):
        log.info('The route /system/status has been triggered')

        json_result = dict()
        json_result["serverVersion"] = self._config.version

        # TODO: uptime, last-update, log-size, mendeley-api-status
        return json.dumps(json_result)

    def get_system_entities(self):
        log.info('The route /system/entities has been triggered')
        json_result = dict()

        return json.dumps(json_result)

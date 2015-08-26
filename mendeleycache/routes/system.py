__author__ = 'kohn'

from flask import Flask
from mendeleycache.data.controller import DataController

from mendeleycache.config import ServiceConfiguration

import json


class SystemController:
    def __init__(self, app: Flask, data_controller: DataController, config: ServiceConfiguration):
        self._app = app
        self._data_controller = data_controller
        self._config = config

    def register(self):
        self._app.add_url_rule('/system', view_func=self.get_system_report)

    def get_system_report(self):
        json_result = dict()
        json_result["server-version"] = self._config.version
        json_result["research-group-id"] = self._config.mendeley.research_group

        # TODO: uptime, last-update, log-size, mendeley-api-status

        return json.dumps(json_result)


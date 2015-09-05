__author__ = 'kohn'

from flask import Flask, request
from mendeleycache.data.controller import DataController

from mendeleycache.config import ServiceConfiguration
from mendeleycache.logging import log
from mendeleycache.pipeline import PipelineController
from mendeleycache.utils.remotes import remote_is_online, get_remote_ip
from mendeleycache.utils.json_encoder import DefaultEncoder

import json


class CacheController:
    def __init__(self, app: Flask,
                 data_controller: DataController,
                 pipeline_controller: PipelineController,
                 config: ServiceConfiguration):
        self._app = app
        self._data_controller = data_controller
        self._pipeline_controller = pipeline_controller
        self._config = config

    def register(self):
        self._app.add_url_rule('/cache/status', methods=['GET'], view_func=self.get_system_status)
        self._app.add_url_rule('/cache/entities', methods=['GET'], view_func=self.get_system_entities)
        self._app.add_url_rule('/cache/update', methods=['POST'], view_func=self.post_update)

    def get_system_status(self):
        log.info('The route GET /cache/status has been triggered')

        api_online = remote_is_online("api.mendeley.com", 443)

        json_result = dict()
        json_result["serverVersion"] = self._config.version
        json_result["mendeleyStatus"] = "online" if api_online else "offline"
        json_result["lastUpdate"] = "never"

        # Fetch last entry in update_log
        last_update_log = self._data_controller.api_data.get_last_update()
        if len(last_update_log) > 0:
            json_result["lastUpdate"] = last_update_log[0]["dt"]

        return json.dumps(json_result, cls=DefaultEncoder)

    def get_system_entities(self):
        log.info('The route GET /cache/entities has been triggered')
        json_result = dict()

        entities = self._data_controller.api_data.get_entities()

        # Serialize fields
        response = []
        for entity in entities:
            columns = dict(entity.items())
            response.append(columns)
        return json.dumps(response, cls=DefaultEncoder)

    def post_update(self):
        log.info('The route POST /cache/update has been triggered')

        # Get remote IP
        remote = get_remote_ip()

        # Trigger the pipeline
        report = self._pipeline_controller.execute(remote)

        # Dump report
        report_dict = dict(report.__dict__)
        json_report = json.dumps(report_dict, cls=DefaultEncoder)
        return json_report

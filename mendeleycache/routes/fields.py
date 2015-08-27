__author__ = 'kohn'

from flask import Flask, request

from mendeleycache.data.controller import DataController

import json


class FieldsController:
    def __init__(self, app: Flask, data_controller: DataController):
        self._app = app
        self._data_controller = data_controller

    def register(self):
        self._app.add_url_rule('/fields', view_func=self.get_fields)

    def get_fields(self):
        fields = self._data_controller.api_data.get_fields()
        response = []
        for field in fields:
            field_json = dict()
            field_json["id"] = field["id"]
            field_json["tile"] = field["title"]
            field_json["cnt"] = field["cnt"]
            response.append(field_json)
        return json.dumps(response)

__author__ = 'kohn'

from flask import Flask, request

from mendeleycache.data.controller import DataController


class FieldsController:
    def __init__(self, app: Flask, data_controller: DataController):
        self._app = app
        self._data_controller = data_controller

    def register(self):
        self._app.add_url_rule('/fields', view_func=self.get_fields)

    def get_fields(self):
        pass

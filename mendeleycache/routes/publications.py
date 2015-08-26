__author__ = 'kohn'

from flask import Flask, request

from mendeleycache.data.controller import DataController


class PublicationsController:
    def __init__(self, app: Flask, data_controller: DataController):
        self._app = app
        self._data_controller = data_controller

    def register(self):
        self._app.add_url_rule('/publications', view_func=self.get_publications)

    def get_publications(self):
        pass

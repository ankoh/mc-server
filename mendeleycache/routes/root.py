__author__ = 'kohn'

from flask import Flask
from mendeleycache.data.controller import DataController

from mendeleycache.config import ServiceConfiguration
from mendeleycache.logging import log

import json


class RootController:
    def __init__(self, app: Flask, data_controller: DataController, config: ServiceConfiguration):
        self._app = app
        self._data_controller = data_controller
        self._config = config

    def register(self):
        self._app.add_url_rule('/', methods=['GET'], view_func=self.get_root)

    def get_root(self):
        log.info('The route / has been triggered')

        return "Welcome to the Mendeley Cache"


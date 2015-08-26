__author__ = 'kohn'

from flask import Flask, request

from mendeleycache.data.controller import DataController


class ProfilesController:
    def __init__(self, app: Flask, data_controller: DataController):
        self._app = app
        self._data_controller = data_controller

    def register(self):
        self._app.add_url_rule('/profiles', view_func=self.get_profiles)

    def get_profiles(self):
        pass

    def get_slim_profiles(self):
        pass

    def get_full_profiles(self):
        pass


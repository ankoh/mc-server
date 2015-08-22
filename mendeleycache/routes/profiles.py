__author__ = 'kohn'

from flask import Flask, request
from flask.ext.sqlalchemy import SQLAlchemy


class ProfilesController:
    def __init__(self, app: Flask, db: SQLAlchemy):
        self.app = app
        self.db = db

    def register(self):
        self.app.add_url_rule('/profiles', view_func=self.get_profiles)

    def get_profiles(self):
        pass

    def get_slim_profiles(self):
        pass

    def get_full_profiles(self):
        pass


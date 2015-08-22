__author__ = 'kohn'

from flask import Flask, request
from flask.ext.sqlalchemy import SQLAlchemy


class PublicationsController:
    def __init__(self, app: Flask, db: SQLAlchemy):
        self.app = app
        self.db = db

    def register(self):
        self.app.add_url_rule('/publications', view_func=self.get_publications)

    def get_publications(self):
        pass

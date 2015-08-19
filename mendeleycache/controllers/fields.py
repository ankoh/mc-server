__author__ = 'kohn'

from flask import Flask, request
from flask.ext.sqlalchemy import SQLAlchemy


class FieldsController:
    def __init__(self, app: Flask, db: SQLAlchemy):
        self.app = app
        self.db = db

    def register(self):
        self.app.add_url_rule('/fields', view_func=self.get_fields)

    def get_fields(self):
        pass

__author__ = 'kohn'

from flask import Flask, request
from flask.ext.sqlalchemy import SQLAlchemy


class SystemController:
    def __init__(self, app: Flask, db: SQLAlchemy):
        self.app = app
        self.db = db

    def register(self):
        self.app.add_url_rule('/system', view_func=self.get_system_report)

    def get_system_report(self):
        pass

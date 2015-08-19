__author__ = 'kohn'

from flask import Flask, request
from flask.ext.sqlalchemy import SQLAlchemy


class StatisticsController:
    def __init__(self, app: Flask, db: SQLAlchemy):
        self.app = app
        self.db = db

    def register(self):
        self.app.add_url_rule('/statistics', view_func=self.get_general_statistics)

    def get_general_statistics(self):
        pass

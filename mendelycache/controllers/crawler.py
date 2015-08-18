__author__ = 'kohn'

from flask import Flask, request
from flask.ext.sqlalchemy import SQLAlchemy


class CrawlerController:
    def __init__(self, app: Flask, db: SQLAlchemy):
        self.app = app
        self.db = db

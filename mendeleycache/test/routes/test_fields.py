__author__ = 'kohn'

import unittest
from os import remove
from os.path import exists

from flask.testing import FlaskClient
from flask.wrappers import Response

from mendeleycache.test.test_app import TestApp
from mendeleycache.app import MendeleyCache

import json


class TestFields(unittest.TestCase):

    def test_get_empty_fields(self):
        TestApp.write_debug_config()
        app = MendeleyCache()

        sut = app.test_client()
        """:type : FlaskClient"""

        # Fire fields versus an empty database
        response= sut.get('/fields', follow_redirects=True)
        """:type : Response"""

        # Check status code
        self.assertEqual(response.status_code, 200)
        # Parse json data
        data=response.get_data(as_text=True)

    def test_get_pipeline_fields(self):
        TestApp.write_debug_config()
        app = MendeleyCache()

        sut = app.test_client()
        """:type : FlaskClient"""

        # Fire fields versus an empty database
        response= sut.get('/fields', follow_redirects=True)
        """:type : Response"""

    def tearDown(self):
        remove(TestApp.config_path) if exists(TestApp.config_path) else None
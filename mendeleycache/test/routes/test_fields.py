__author__ = 'kohn'

import unittest
from os import remove
from os.path import exists

from flask.testing import FlaskClient
from flask.wrappers import Response

from mendeleycache.test.test_app import TestApp
from mendeleycache.app import MendeleyCache

import json
import time


class TestFields(unittest.TestCase):
    def test_get_empty_fields(self):
        TestApp.write_debug_config()
        app = MendeleyCache()
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
        app.testing = True

        sut = app.test_client()
        """:type : FlaskClient"""

        # Fire fields versus an empty database
        response= sut.get('/fields', follow_redirects=True)
        """:type : Response"""

        self.assertEqual(response.status_code, 200)
        data = response.get_data(as_text=True)
        json_data = json.loads(data)
        self.assertEqual(len(json_data), 0)

        # Trigger the pipeline
        app.pipeline_controller.execute()

        # Fire fields versus a filled database
        response= sut.get('/fields', follow_redirects=True)
        """:type : Response"""

        self.assertEqual(response.status_code, 200)
        data = response.get_data(as_text=True)
        json_data = json.loads(data)
        self.assertEqual(len(json_data), 4)

    def tearDown(self):
        remove(TestApp.config_path) if exists(TestApp.config_path) else None
__author__ = 'kohn'

import unittest
from os import remove
from os.path import exists

from flask.testing import FlaskClient
from flask.wrappers import Response

from mendeleycache.test.test_app import TestApp
from mendeleycache.mendeleycache import MendeleyCache

import json


class TestSystem(unittest.TestCase):

    def test_get_system(self):

        app = MendeleyCache('mendeleycache')
        app.debug = True
        sut = app.test_client()
        """:type : FlaskClient"""

        response= sut.get('/system/status', follow_redirects=True)
        """:type : Response"""

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Parse json data
        data=response.get_data(as_text=True)
        response_json = json.loads(data)

        self.assertIn('serverVersion', response_json)

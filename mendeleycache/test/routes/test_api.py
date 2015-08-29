__author__ = 'kohn'

import unittest
from os import remove
from os.path import exists

from flask.testing import FlaskClient
from flask.wrappers import Response

from mendeleycache.test.test_app import TestApp
from mendeleycache.mendeleycache import MendeleyCache

import json
import time


def sample_api():
    TestApp.write_debug_config()
    app = MendeleyCache('mendeleycache')
    app.debug = True
    app.pipeline_controller.execute()

    sut = app.test_client()
    """:type : FlaskClient"""

    calls = [
        '/fields',
        '/profiles?slim=true',
        str('/profiles'
            '?field-ids=Y29udGludW91c3NvZnR3YXJlZW5naW5lZXJpbmc%3D'),
        str('/profiles'
            '?profile-ids=Y29uc3RhbnRpbnNjaGV1ZXJtYW5u'
            '&field-ids=Y29udGludW91c3NvZnR3YXJlZW5naW5lZXJpbmc%3D'),
        '/profiles'
    ]

    for call in calls:
        response= sut.get(call, follow_redirects=True)
        """:type : Response"""
        data = response.get_data(as_text=True)
        json_data = json.loads(data)
        print('Results for REST call: %s' % call)
        print(json.dumps(json_data, indent=2))

    remove(TestApp.config_path) if exists(TestApp.config_path) else None

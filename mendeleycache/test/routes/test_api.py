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
import sys


def sample_api():
    app = MendeleyCache('mendeleycache')
    app.debug = True
    report = app.pipeline_controller.execute()

    sut = app.test_client()
    """:type : FlaskClient"""

    calls = [
        '/fields/',
        '/profiles/?slim=true',
        '/profiles/',
        str('/profiles/'
            '?field-ids=Y29udGludW91c3NvZnR3YXJlZW5naW5lZXJpbmc%3D'),
        str('/profiles/'
            '?profile-ids=Y29uc3RhbnRpbnNjaGV1ZXJtYW5u'
            '&field-ids=Y29udGludW91c3NvZnR3YXJlZW5naW5lZXJpbmc%3D'),
        '/documents/',
        str(
            '/documents/'
            '?profile-ids=c3RlcGhhbmtydXNjaGU%3D'
            '&field-ids=Y29udGludW91c3NvZnR3YXJlZW5naW5lZXJpbmc%3D'
        ),
        str(
            '/documents/'
            '?profile-ids=c3RlcGhhbmtydXNjaGU%3D'
            '&field-ids=Y29udGludW91c3NvZnR3YXJlZW5naW5lZXJpbmc%3D'
            '&limit=1&offset=1'
        ),
        str(
            '/documents/'
            '?profile-ids=c3RlcGhhbmtydXNjaGU%3D'
            '&field-ids=Y29udGludW91c3NvZnR3YXJlZW5naW5lZXJpbmc%3D'
            '&limit=1&order-attr=year&order-dir=desc'
        ),
        str(
            '/documents/'
            '?profile-ids=c3RlcGhhbmtydXNjaGU%3D'
            '&field-ids=Y29udGludW91c3NvZnR3YXJlZW5naW5lZXJpbmc%3D'
            '&limit=1&order-attr=title'
        ),
        str(
            '/documents/'
            '?profile-ids=c3RlcGhhbmtydXNjaGU%3D'
            '&field-ids=Y29udGludW91c3NvZnR3YXJlZW5naW5lZXJpbmc%3D'
            '&limit=1&order-attr=source'
        ),
        str(
            '/documents/'
            '?profile-ids=c3RlcGhhbmtydXNjaGU%3D'
            '&field-ids=Y29udGludW91c3NvZnR3YXJlZW5naW5lZXJpbmc%3D'
            '&limit=1&order-attr=source&only-count=true'
        ),
        str(
            '/documents/'
            '?order-attr=year&order-dir=desc&offset=5&limit=5&only-count=true'
        ),
        '/cache/status/',
        '/cache/entities/'
    ]

    for call in calls:
        response = sut.get(call, follow_redirects=True)
        """:type : Response"""
        data = response.get_data(as_text=True)
        json_data = json.loads(data)
        print('Results for REST call: GET %s' % call)
        print(json.dumps(json_data, indent=2))

    response = sut.post('/cache/update/', follow_redirects=True)
    """:type : Response"""
    data = response.get_data(as_text=True)
    json_data = json.loads(data)
    print('Results for REST call: POST /cache/update')
    print(json.dumps(json_data, indent=2))

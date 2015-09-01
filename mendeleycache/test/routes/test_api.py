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
    app = MendeleyCache('mendeleycache')
    app.debug = True
    app.pipeline_controller.execute()

    sut = app.test_client()
    """:type : FlaskClient"""

    calls = [
        '/fields',
        '/profiles?slim=true',
        '/profiles',
        str('/profiles'
            '?field-ids=Y29udGludW91c3NvZnR3YXJlZW5naW5lZXJpbmc%3D'),
        str('/profiles'
            '?profile-ids=Y29uc3RhbnRpbnNjaGV1ZXJtYW5u'
            '&field-ids=Y29udGludW91c3NvZnR3YXJlZW5naW5lZXJpbmc%3D'),
        '/documents',
        str(
            '/documents'
            '?profile-ids=c3RlcGhhbmtydXNjaGU%3D'
            '&field-ids=Y29udGludW91c3NvZnR3YXJlZW5naW5lZXJpbmc%3D'
        ),
        str(
            '/documents'
            '?profile-ids=c3RlcGhhbmtydXNjaGU%3D'
            '&field-ids=Y29udGludW91c3NvZnR3YXJlZW5naW5lZXJpbmc%3D'
            '&limit=1&offset=1'
        ),
        str(
            '/documents'
            '?profile-ids=c3RlcGhhbmtydXNjaGU%3D'
            '&field-ids=Y29udGludW91c3NvZnR3YXJlZW5naW5lZXJpbmc%3D'
            '&limit=1&order-attr=year&order-dir=desc'
        ),
        str(
            '/documents'
            '?profile-ids=c3RlcGhhbmtydXNjaGU%3D'
            '&field-ids=Y29udGludW91c3NvZnR3YXJlZW5naW5lZXJpbmc%3D'
            '&limit=1&order-attr=title'
        ),
        str(
            '/documents'
            '?profile-ids=c3RlcGhhbmtydXNjaGU%3D'
            '&field-ids=Y29udGludW91c3NvZnR3YXJlZW5naW5lZXJpbmc%3D'
            '&limit=1&order-attr=source'
        ),
        str(
            '/documents'
            '?profile-ids=c3RlcGhhbmtydXNjaGU%3D'
            '&field-ids=Y29udGludW91c3NvZnR3YXJlZW5naW5lZXJpbmc%3D'
            '&limit=1&order-attr=source&only-count=true'
        ),
        '/system/status',
        '/system/entities'

    ]

    for call in calls:
        response= sut.get(call, follow_redirects=True)
        """:type : Response"""
        data = response.get_data(as_text=True)
        json_data = json.loads(data)
        print('Results for REST call: %s' % call)
        print(json.dumps(json_data, indent=2))

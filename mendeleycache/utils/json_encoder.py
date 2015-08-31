__author__ = 'kohn'

from datetime import datetime
import json


class DefaultEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)

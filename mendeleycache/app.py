__author__ = 'kohn'

from mendeleycache.mendeleycache import MendeleyCache
from flask.ext.cors import CORS

app = MendeleyCache(__name__)

# Allow cross origin site requests on all routes
CORS(app)

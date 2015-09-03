__author__ = 'kohn'

from mendeleycache.mendeleycache import MendeleyCache
import flask

app = MendeleyCache(__name__)


@app.before_request
def before():
    flask.request.environ['CONTENT_TYPE'] = 'application/json'


# Uncomment this, if you need CORS support.
# As this docker container is used through nginx reverse proxies anyway, i wont set the header twice here
# @app.after_request
# def add_cors(resp):
#     """
#     Ensure all responses have the CORS headers. This ensures any failures are also accessible
#     by the client.
#     http://mortoray.com/2014/04/09/allowing-unlimited-access-with-cors/
#     """
#     resp.headers['Access-Control-Allow-Origin'] = flask.request.headers.get('Origin', '*')
#     resp.headers['Access-Control-Allow-Credentials'] = 'true'
#     resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET'
#     resp.headers['Access-Control-Allow-Headers'] = flask.request.headers.get(
#         'Access-Control-Request-Headers', 'Authorization')
#     return resp

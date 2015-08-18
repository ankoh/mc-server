__author__ = 'kohn'

from flask import Blueprint


blueprint = Blueprint('publications', __name__)


@blueprint.route('/')
def test():
    return 'Hello Publications'

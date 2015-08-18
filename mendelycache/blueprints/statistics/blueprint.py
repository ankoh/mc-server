__author__ = 'kohn'

from flask import Blueprint


blueprint = Blueprint('statistics', __name__)


@blueprint.route('/')
def test():
    return 'Hello Statistics'

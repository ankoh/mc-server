__author__ = 'kohn'

from flask import Blueprint


blueprint = Blueprint('fields', __name__)


@blueprint.route('/')
def test():
    return 'Hello Fields'

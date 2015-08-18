__author__ = 'kohn'

from flask import Blueprint


blueprint = Blueprint('system', __name__)


@blueprint.route('/')
def test():
    return 'Hello System'

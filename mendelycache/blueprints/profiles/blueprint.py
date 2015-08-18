__author__ = 'kohn'

from flask import Blueprint


blueprint = Blueprint('profiles', __name__)


@blueprint.route('/')
def test():
    return 'Hello Profiles'

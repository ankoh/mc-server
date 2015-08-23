__author__ = 'kohn'

from os.path import dirname, join

BASE = dirname(dirname(__file__))


def get_relative_path(*path):
    """
    Construct the path relative to the project root
    get_path('samples', 'groups', '42.json')
    :param path: path components that build the path relative to the project root
    :return: return os path
    """
    return join(BASE, *path)


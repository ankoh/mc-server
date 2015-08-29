__author__ = 'kohn'

from datetime import datetime


def string_to_bool(v):
    return v.lower() in ("yes", "true", "t", "1")


def datetime_to_sqltime(dt: datetime):
    return dt.strftime('%Y-%m-%d %H:%M:%S')

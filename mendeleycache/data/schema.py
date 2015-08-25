__author__ = 'kohn'

from mendeleycache.utils.files import get_relative_path
import re

from mendeleycache.utils.regex import sql_comments, multi_whitespace


def read_sqlite_schema() -> [str]:
    """
    Reads sqlite schema and splits ;
    :return:
    """
    path = get_relative_path('sql', 'schema', 'sqlite.sql')
    return read_schema(path)


def read_mysql_schema() -> [str]:
    """
    Reads mysql schema and splits ;
    :return:
    """
    path = get_relative_path('sql', 'schema', 'mysql.sql')
    return read_schema(path)


def read_schema(path) -> [str]:
    """
    Read file and split semicolons
    :param path:
    :return:
    """
    with open(path, "r") as schema_file:
        schema = schema_file.read()
        schema = re.sub(sql_comments, '', schema)
        schema = re.sub(multi_whitespace, ' ', schema)
        return schema.replace('\n', '').split(';')

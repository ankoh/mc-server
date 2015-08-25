__author__ = 'kohn'

from mendeleycache.utils.files import get_relative_path
from mendeleycache.utils.regex import clean_single_sql


def read_single_statement_sql_path(path) -> str:
    with open(path, "r") as sql_file:
        sql = sql_file.read()
        return clean_single_sql(sql)


def read_single_statement_sql_file(*path) -> str:
    sql_file_path = get_relative_path(*path)
    return read_single_statement_sql_path(sql_file_path)
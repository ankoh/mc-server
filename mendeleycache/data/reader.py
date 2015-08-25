__author__ = 'kohn'

from mendeleycache.utils.files import get_relative_path

import re

sql_comments = re.compile('--[A-Za-z0-9_ \-]*\n')
multi_whitespace = re.compile(' +')


def clean_sql(sql: str) -> str:
    result = re.sub(sql_comments, ' ', sql)
    result = result.replace('\n', ' ')
    result = re.sub(multi_whitespace, ' ', result)
    return result


def read_sql_statements(*path) -> [str]:
    """
    Given a file path this method reads the sql file at that location,
    cleans the sql statements (whitespace/comments)
    and splits statements via semicolon.
    Subsequently all the empty statements are removed
    :param path:
    :return:
    """
    sql_file_path = get_relative_path(*path)
    with open(sql_file_path, "r") as sql_statements_file:
        sql_statements_string = sql_statements_file.read()
        sql_statements_string = clean_sql(sql_statements_string)
        sql_statements = sql_statements_string.split(';')
        result = [stmt for stmt in sql_statements if stmt and not stmt.isspace()]
        return result
__author__ = 'kohn'

import re

sql_comments = re.compile('--[A-Za-z0-9_ \-]*\n')
multi_whitespace = re.compile(' +')


def clean_single_sql(sql: str):
    sql = re.sub(sql_comments, ' ', sql)
    sql = sql.replace('\n', ' ')
    sql = re.sub(multi_whitespace, ' ', sql)
    return sql
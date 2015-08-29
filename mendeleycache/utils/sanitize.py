__author__ = 'kohn'

import re


def sanitize_text(sql_input: str) -> str:
    result = sql_input

    # Double the ticks
    result = re.sub('\'', '\'\'', result)
    return result


def sanitize_stmt(sql_input: str) -> str:
    return sql_input

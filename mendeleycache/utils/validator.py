__author__ = 'kohn'

import re

pattern_mendeley_id = re.compile('^\w+(-\w+)+$')


def is_valid_mendeley_id(m_id: str) -> bool:
    return pattern_mendeley_id.match(m_id)

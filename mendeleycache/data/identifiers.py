__author__ = 'kohn'

import base64


def generate_id(unified_string: str) -> str:
    binary = bytes(unified_string, 'utf-8')
    b64 = base64.b64encode(binary)
    return b64.decode('utf-8')

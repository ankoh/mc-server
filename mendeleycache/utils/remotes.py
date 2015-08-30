__author__ = 'kohn'

import socket


def remote_is_online(hostname: str, port: int) -> bool:
    """
    Checks whether the remote is online or not
    :param hostname:
    :param port:
    :return:
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    online = False
    try:
        sock.connect((hostname, port))
        online = True
    except socket.error as e:
        online = False
    sock.close()
    return online

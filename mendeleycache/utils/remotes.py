__author__ = 'kohn'

from flask import request

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


def get_remote_ip():
    """
    Given a flask request, extracts the remote address
    :param request:
    :return:
    """
    # Enter your trusted proxy here.
    # With a local NGINX reverse proxy that's localhost
    # Be aware of that issue:
    # http://stackoverflow.com/questions/22868900/how-do-i-safely-get-the-users-real-ip-address-in-flask-using-mod-wsgi
    # Otherwise spoofing becomes dangerous
    trusted_proxies = {
        '127.0.0.1'
    }
    route = request.access_route + [request.remote_addr]

    remote_addr = next((addr for addr in reversed(route)
                        if addr not in trusted_proxies), request.remote_addr)
    return remote_addr
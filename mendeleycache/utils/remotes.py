__author__ = 'kohn'

from flask import request

import re
import socket

from mendeleycache.logging import log


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

# Precompile a list of trusted proxies
# Localhost and the 172.17/16 subnet are trusted by default
trusted_proxies = {
    re.compile('127.0.0.1'),
    re.compile('localhost'),
    re.compile('172.17.[0-9]+.[0-9]+')
}


def is_trusted_proxy(addr: str) -> bool:
    if addr is None:
        return False
    log.debug("Checking if address '%s' is a trusted proxy" % addr)
    for trusted_proxy in trusted_proxies:
        if trusted_proxy.match(addr):
            return True
    return False


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

    route = request.access_route + [request.remote_addr]
    log.debug("Route: %s" % route)
    remote_addr = next((addr for addr in reversed(route)
                        if not is_trusted_proxy(addr)), request.remote_addr)
    log.debug("Choosing: '%s'" % remote_addr)
    return remote_addr

import os
import socket
from urllib.parse import urlparse

import socks

# If socks_proxy is set in environment variable then,
# this script replaces the default socket to route through
# socks proxy

DEFAULT_SOCKET = socket.socket


def get_proxy():
    proxy = os.environ.get('socks_proxy')
    if proxy:
        parsed_url = urlparse(proxy)
        host = parsed_url.hostname
        port = parsed_url.port
        if host and port:
            return host, port
        return None
    else:
        return None


def override_socket():
    proxy_settings = get_proxy()
    if proxy_settings:
        host, port = proxy_settings
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, host, port)
        socket.socket = socks.socksocket


def remove_socket_override():
    socket.socket = DEFAULT_SOCKET


override_socket()

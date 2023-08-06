import socket


def get_hostip():
    try:
        host_ip = socket.gethostbyname(socket.gethostname())
    except:
        host_ip = ''

    return host_ip


def get_hostname():
    try:
        hostname = socket.gethostname()
    except:
        hostname = ''

    return hostname

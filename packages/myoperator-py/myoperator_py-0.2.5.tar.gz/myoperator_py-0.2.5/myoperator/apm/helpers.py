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


def get_generic_url_from_django_route_path(request_path, param_dict):
    """
        Takes a request path of the form "/path/api/1/xyx/2" and converts it into generic paths with 1 and 2 being replaced with their placeholders provided in param_dict as 'name_of_placeholder': '<value_in_url>' dict.
        Such param dict can be obtained by calling django.url.resolve method on the real path and its kwargs property will be the param dict.

        Attributes:
        ----------
        request_path str: real request path without placeholders e.g /path/api/user/1
        param_dict dict: dictionary with 'placholder': '<value of placeholder in url>'
                    key-value pairs
    """

    for param, value in param_dict.items():
        request_path = request_path.replace(value, param)

    return request_path

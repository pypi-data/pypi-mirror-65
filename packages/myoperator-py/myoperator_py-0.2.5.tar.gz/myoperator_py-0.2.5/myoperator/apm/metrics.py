import os
import logging
import uuid

import statsd

from .helpers import get_hostname, get_hostip
from .constants import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

STATSD_CLIENT_HOST = os.environ.get('STATSD_CLIENT_HOST', 'localhost')
STATSD_CLIENT_PORT = os.environ.get('STATSD_CLIENT_PORT', 9125)
logger.debug("STATSD HOST: {} STATSD PORT".format(
    STATSD_CLIENT_HOST, STATSD_CLIENT_PORT))

# if not found give a random app_name
APP_NAME = os.environ.get(METRIC_APP_NAME_VAR_NAME, uuid.uuid4().hex)
SERVER_IP = os.environ.get('METRIC_SERVER_IP', get_hostip())
SERVER_NAME = os.environ.get('METRIC_SERVER_NAME', get_hostname())

CURRENT_ENTRY_POINT = ''

logger.debug('Default metric APP_NAME: {}'.format(APP_NAME))
logger.debug('Default metric SERVER_IP {}'.format(SERVER_IP))
logger.debug('Default metric SERVER_NAME: {}'.format(SERVER_NAME))

statsd_client = statsd.StatsClient(STATSD_CLIENT_HOST, STATSD_CLIENT_PORT)


def set_entry_point(entry_point):
    """
        Sets the entry_point tag(request url, cli name etc) for all the metrics in collected through the apm library.
        If the django middleware is being used you probably don't need to set this.
        However in other cases where the middleware is not used e.g non-django applications or cli applications
        it can be explicitly set using this function.
        For http requests it needs to be the relative path of the api(e.g /api/auth),
        for cli applications/library it can be custom set.
    """
    global CURRENT_ENTRY_POINT
    CURRENT_ENTRY_POINT = entry_point


def config_client(protocol='UDP', host=STATSD_CLIENT_HOST, port=STATSD_CLIENT_PORT, config_dict=None, tcp_timeout=1.0):
    """
        Function to change the protocol, host and other settings used by the apm client at runtime to push metrics.
        Default protocol is UDP and it's suggested to be used in all cases as it's non blocking.
        Other settings that can be changed are the common labels/tags for all metrics such as server_ip, server_name,
        app_name.

        Attributes:
        ----------
        protocol str: can be UDP or TCP
        host: change the statsd host
        port: change the statsd port
        config_dict dict: {
                            'server_ip': IP of the server defaults to host IP(default will be meangingless in case of docker),
                            'server_name': human readable name of the server defaults to,
                            'app_name': the unique name of the app for which metrics are being measured.
                        }
                        All these keys will be available as a dropdown in grafana UI to filter metrics.
                        app_name key is required to be present.

        tcp_timeout float: It is only applicable if protocol is TCP
    """
    global statsd_client
    if protocol == 'UDP':
        statsd_client = statsd.StatsClient(host, port)
    elif protocol == 'TCP':
        statsd_client = statsd.TCPStatsClient(
            host=host, port=port, timeout=tcp_timeout)

    if not config_dict:
        config_dict = {}
    global APP_NAME
    global SERVER_IP
    global SERVER_NAME
    APP_NAME = config_dict.get('app_name', APP_NAME)
    SERVER_IP = config_dict.get('server_ip', SERVER_IP)
    SERVER_NAME = config_dict.get('server_name', SERVER_NAME)

    logger.debug('Configured metric APP_NAME: {}'.format(APP_NAME))
    logger.debug('Configured metric SERVER_IP {}'.format(SERVER_IP))
    logger.debug('Configured metric SERVER_NAME: {}'.format(SERVER_NAME))
    logger.debug(type(statsd_client))


def add_label_to_metric_without_mapping(metric_name, labels_dict):
    """
        Add labels to the given metric_name uisng the Librato-style tags.
        Attributes:
        ----------
        metric_name str: metric name string to which the tags are to be added
        labels_dict dict: {
                            <label/tag name>: <label_value>
                        }

                        For this key would be the label/tag name and the value will be its value.
                        These key/value pairs will be converted to Prometheus labels.
    """
    if METRIC_NO_MAPPING_LABEL_PREFIX not in metric_name:
        metric_name += METRIC_NO_MAPPING_LABEL_PREFIX
    else:
        metric_name += ','

    labels_str = ''
    labels_list = []
    for key, value in labels_dict.items():
        labels_list.append('{}{}{}'.format(
            key, METRIC_NO_MAPPING_LABEL_EQUAL, value))

    labels_str = METRIC_NO_MAPPING_LABEL_SEPERATOR.join(labels_list)
    metric_name += labels_str
    return metric_name


def add_common_labels_to_metric(metric_name):
    """
        Adds common labels to the given metric.
    """
    global CURRENT_ENTRY_POINT
    global SERVER_IP
    global SERVER_NAME
    common_labels = {
        'entry_point': CURRENT_ENTRY_POINT,
        'server_ip': SERVER_IP,
        'server_name': SERVER_NAME
    }
    metric_name = add_label_to_metric_without_mapping(
        metric_name, common_labels)
    return metric_name


def add_common_labels_to_all_metrics(metric_name, seperator=METRIC_NAME_SEPERATOR):
    global APP_NAME
    metric_name = add_label_to_metric_name(APP_NAME, metric_name)
    metric_name = add_common_labels_to_metric(metric_name)
    return metric_name


def add_label_to_metric_name(label, metric_name, seperator=METRIC_LABEL_SEPERATOR):
    return metric_name + seperator + label


def create_http_request_latency_histogram_metric(metric_name=BASE_HTTP_LATENCY_METRIC_NAME):
    metric_name = add_common_labels_to_all_metrics(metric_name)
    return metric_name


def create_http_request_counter_metric_name(metric_name=BASE_HTTP_COUNTER_METRIC_NAME):
    metric_name = add_common_labels_to_all_metrics(metric_name)
    return metric_name


def create_http_request_latency_gauge_metric_name(metric_name=BASE_HTTP_LATENCY_GAUGE_METRIC_NAME):
    metric_name = add_common_labels_to_all_metrics(metric_name)
    return metric_name


def create_external_io_duration_metric_name(metric_name=BASE_EXTERNAL_IO_DURATION_METRIC_NAME):
    metric_name = add_common_labels_to_all_metrics(metric_name)
    return metric_name


def create_external_io_counter_metric_name(metric_name=BASE_EXTERNAL_IO_COUNTER_METRIC_NAME):
    metric_name = add_common_labels_to_all_metrics(metric_name)
    return metric_name


def create_external_io_exception_metric_name(metric_name=BASE_EXTERNAL_IO_EXCEPTION_METRIC):
    metric_name = add_common_labels_to_all_metrics(metric_name)
    return metric_name


def create_http_requests_exception_metric_name(metric_name=BASE_HTTP_EXCEPTION_METRIC):
    metric_name = add_common_labels_to_all_metrics(metric_name)
    return metric_name


def create_function_duration_metric_name(metric_name=BASE_FUNCTION_DURATION_METRIC_NAME):
    metric_name = add_common_labels_to_all_metrics(metric_name)
    return metric_name


def create_function_exception_metric_name(metric_name=BASE_FUNCTION_EXCEPTION_METRIC):
    metric_name = add_common_labels_to_all_metrics(metric_name)
    return metric_name


def create_http_function_latency_gauge_metric_name(metric_name=BASE_FUNCTION_LATENCY_GAUGE_METRIC):
    metric_name = add_common_labels_to_all_metrics(metric_name)
    return metric_name


def create_external_service_latency_gauge_metric_name(metric_name=BASE_EXTERNAL_IO_LATENCY_GAUGE_METRIC):
    metric_name = add_common_labels_to_all_metrics(metric_name)
    return metric_name


def create_bytes_metric_name(metric_name=BASE_BYTES_METRIC):
    metric_name = add_common_labels_to_all_metrics(metric_name)
    return metric_name


def create_http_request_metrics(status_code, duration_ms, exception_type_class=None):
    """
        Pushes duration metrics for http requests. Creates three types of metrics:
        1. Request Duration Histogram metrics
        2. Request Duration Gauge metrics(raw value in ms)
        3. Exception type counter metric is created if exception_type_class is provided and status_code is in range (500, 599)

        Attributes:
        -----------
        status_code int: Can only be valid http status code (200, 599)
        duartion_ms float: Time taken for request in milliseconds

        Returns tuple: (<histogram_metric_name>, <guage_metric_name>, <exception_metric_name>)
                        exception_metric_name is None is status code is other than range (500, 599)
                        and no exception_type_class is provided.
    """
    if status_code not in HTTP_REQUEST_STATUS_CODE_OPTIONS:
        logger.warning('status_code can only be one of {}'.format(
            ', ', join(HTTP_REQUEST_STATUS_CODE_OPTIONS)))

    exception_metric = None
    if status_code >= 500:
        status_code = str(status_code)
        if exception_type_class:
            exception_metric = create_http_requests_exception_metric_name()
            exception_metric = add_label_to_metric_without_mapping(
                exception_metric, {'exception_class': exception_type_class})

            statsd_client.incr(exception_metric)
            logger.debug('Incremented metric {}'.format(exception_metric))

    status_code = str(status_code)
    hist_request_duration = create_http_request_latency_histogram_metric()
    hist_request_duration = add_label_to_metric_without_mapping(hist_request_duration,
                                                                {
                                                                    'status_code': status_code,
                                                                })

    statsd_client.timing(hist_request_duration, duration_ms)
    logger.debug('Created histogram http metric {} with value {}'.format(
        hist_request_duration, duration_ms))

    request_duration_gauge_metric = create_http_request_latency_gauge_metric_name()
    request_duration_gauge_metric = add_label_to_metric_without_mapping(
        request_duration_gauge_metric, {'status_code': status_code})

    statsd_client.gauge(request_duration_gauge_metric, duration_ms)
    logger.debug('Created gauge http duration metric {} with value {}'.format(
        request_duration_gauge_metric, duration_ms))
    return hist_request_duration, request_duration_gauge_metric, exception_metric


def create_http_request_counter_metric(status_code):
    """
        Increments a simple counter metric to track the number of requests made.
    """
    if status_code not in HTTP_REQUEST_STATUS_CODE_OPTIONS:
        logger.warning('status_code can only be one of {}'.format(
            ', ', join(HTTP_REQUEST_STATUS_CODE_OPTIONS)))

    status_code = str(status_code)
    request_counter_metric = create_http_request_counter_metric_name()
    request_counter_metric = add_label_to_metric_without_mapping(
        request_counter_metric,
        {'status_code': status_code})
    statsd_client.incr(request_counter_metric)
    logger.debug('Created metric: request counter {}'.format(
        request_counter_metric))


def create_function_duration_metrics(duration_ms, function_name, status, exception_type_class=None):
    """
        1. Pushes a Histogram based metric for functions runtime.
        2. If the status is 'error', creates a exception type counter with exception_type_class as label.
        3. It also creates a gauge based metric for function duration to capture raw function runtime values, It's always created.

        Attributes:
        -----------
        status str: can be either 'success' or 'error'.
        function_name str: label value to be added added to the metrics generated with the name 'function_name'
        exception_type_class str: required if status is 'error'. Name of the exception type class.
    """
    if status not in FUNCTION_STATUS_VALUES:
        logger.warning('status can only be one of [{}]'.format(
            ', '.join(FUNCTION_STATUS_VALUES)))

    exception_metric = None

    if status == FUNCTION_STATUS_VALUES[1]:
        if not exception_type_class:
            logger.warning(
                'exception_type_class cannot be null if status is "error"')
        else:
            exception_metric = create_function_exception_metric_name()
            exception_metric = add_label_to_metric_without_mapping(exception_metric,
                                                                   {'function_name': function_name,
                                                                    'host': host,
                                                                    'exception_class': exception_type_class
                                                                    })
            statsd_client.incr(exception_metric)
            logger.debug('Incremented metric {}'.format(exception_metric))

    hist_metric = create_function_duration_metric_name()
    hist_metric = add_label_to_metric_without_mapping(hist_metric, {
        'function_name': function_name,
        'host': host,
        'status': status
    })

    function_duration_gauge_metric = create_http_function_latency_gauge_metric_name()
    function_duration_gauge_metric = add_label_to_metric_without_mapping(function_duration_gauge_metric, {
        'function_name': function_name,
        'host': host,
        'status': status
    })

    statsd_client.gauge(function_duration_gauge_metric, duration_ms)
    logger.debug('Created guage function duration metric {} with value {}'.format(
        function_duration_gauge_metric, duration_ms))

    statsd_client.timing(hist_metric, duration_ms)
    logger.debug('Pushed function duration histogram metric {} with value {}'.format(
        hist_metric, duration_ms))

    return hist_metric, function_duration_gauge_metric, exception_metric


def create_external_service_duration_metrics(status, duration_ms, name, address,
                                             tag, exception_type=None):
    """
        Creates metrics related to runtime of external services and exceptions raised for the same.
        Creates two metrics:
        1. Histogram based duration metric with duration in ms as the value.
        2. Counter based exception metric to count types of Exception raised during the external service call. Only created if status is 'error'.

        Attributes:
        status str: Value can only be in ['success', 'error'].
        duration_ms float: Duration for which the service ran in milliseconds.
        name: Name of the service which will be added as label for the metric with the same name.
        address: The address of the service which is being called. Added as a label with the same name.
        tag: can be any one of tags defined in the constants.py file.
        exception_type str: Name of the exception class raised if the status is 'error' otherwise its not required.
    """
    if status not in FUNCTION_STATUS_VALUES:
        logger.warning('status can only be one of [{}]'.format(
            ', '.join(FUNCTION_STATUS_VALUES)))

    exception_metric = None
    if status == FUNCTION_STATUS_VALUES[1]:
        if not exception_type:
            logger.warning('exception_type cannot be null for status="error"')
        else:
            exception_metric = create_external_io_exception_metric_name()
            exception_metric = add_label_to_metric_without_mapping(exception_metric, {
                'name': name,
                'address': address,
                'exception_class': exception_type,
                'external_tag': tag
            })
            statsd_client.incr(exception_metric)
            logger.debug('Incremented metric {}'.format(exception_metric))

    hist_metric = create_external_io_duration_metric_name()
    hist_metric = add_label_to_metric_without_mapping(hist_metric, {
        'name': name,
        'address': address,
        'status': status
    })

    statsd_client.timing(hist_metric, duration_ms)
    logger.debug('Pushed histogram metric {} with value {}'.format(
        hist_metric, duration_ms))

    service_duration_gauge_metric = create_external_service_latency_gauge_metric_name()
    service_duration_gauge_metric = add_label_to_metric_without_mapping(service_duration_gauge_metric, {
        'name': name,
        'address': address,
        'status': status
    })

    statsd_client.gauge(service_duration_gauge_metric, duration_ms)
    logger.debug('Created gauge external service duration metric {} with value {}'.format(
        service_duration_gauge_metric, duration_ms))
    return hist_metric, service_duration_gauge_metric, exception_metric


def create_bytes_metric(size_in_bytes, name_label):
    """
        Function to push bytes metric.
        Attributes:
        ----------
        name_label: label to identify which component/module/function etc is being measured. <b> Cannot contain special charaters except _ .

    """
    metric_name = create_bytes_metric_name()
    metric_name = add_label_to_metric_without_mapping(metric_name, {
        'name': name_label
    })

    statsd_client.gauge(metric_name, size_in_bytes)
    logger.debug('Created gauge bytes metric {} with value {}'.format(
        metric_name, size_in_bytes))

    return metric_name


def create_external_io_counter_metric(name, address, tag):
    external_io_counter = create_external_io_counter_metric_name()
    external_io_counter = add_label_to_metric_without_mapping(external_io_counter, {
        'name': name,
        'address': address,
        'tag': tag
    })

    statsd_client.incr(external_io_counter)
    logger.debug('Incremented histogram metric {}'.format(external_io_counter))

    return external_io_counter

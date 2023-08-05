import os
import logging

import statsd
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)

STATSD_CLIENT_HOST = os.environ.get('STATSD_CLIENT_HOST', 'localhost')
STATSD_CLIENT_PORT = os.environ.get('STATSD_CLIENT_PORT', 9125)

logger.info("STATDS HOST: {}".format(STATSD_CLIENT_HOST))

statsd_client = statsd.StatsClient(STATSD_CLIENT_HOST, STATSD_CLIENT_PORT)

def config_client(protocol='UDP', host=STATSD_CLIENT_HOST, port=STATSD_CLIENT_PORT, timeout=1.0):
    """
        Function to change the protocol, host and other settings used by the apm client at runtime to push metrics. Default is UDP

        Attributes:
        ----------
        protocol str: can be UDP or TCP
        host: change the statsd host
        port: change the statsd port
        timeout float: It is only applicable if protocol is TCP
    """
    global statsd_client
    if protocol == 'UDP':
        statsd_client = statsd.StatsClient(host, port)
    elif protocol == 'TCP':
        statsd_client = statsd.TCPStatsClient(host=host, port=port, timeout=timeout)

logger.info(type(statsd_client))

BASE_HTTP_LATENCY_METRIC_NAME = 'http_requests_duration_ms'
BASE_HTTP_COUNTER_METRIC_NAME = 'http_requests_total'
BASE_HTTP_LATENCY_GAUGE_METRIC_NAME =  'http_requests_duration_ms_total'
BASE_EXTERNAL_IO_DURATION_METRIC_NAME = 'external_io_duration_ms'
BASE_EXTERNAL_IO_LATENCY_GAUGE_METRIC = 'external_io_duration_ms_total'
BASE_EXTERNAL_IO_COUNTER_METRIC_NAME = 'external_io_total'
BASE_FUNCTION_DURATION_METRIC_NAME = 'function_duration_ms'

BASE_HTTP_EXCEPTION_METRIC = 'http_requests_exception_type'
BASE_EXTERNAL_IO_EXCEPTION_METRIC = 'external_io_exception_type'
BASE_FUNCTION_EXCEPTION_METRIC = 'function_exception_type'
BASE_FUNCTION_LATENCY_GAUGE_METRIC = 'function_duration_ms_total'

BASE_BYTES_METRIC = 'bytes_size'

METRIC_NAME_SEPERATOR = '_'
METRIC_LABEL_SEPERATOR = '.'

HTTP_REQUEST_STATUS_CODE_OPTIONS = range(200,599)
FUNCTION_STATUS_VALUES = ['success', 'error']

def prefix_metric_name(prefix, metric_name, seperator=METRIC_NAME_SEPERATOR):
    return prefix + seperator + metric_name

def add_label_to_metric_name(label, metric_name, seperator=METRIC_LABEL_SEPERATOR):
    return metric_name + seperator + label

def create_http_request_latency_histogram_metric(metric_prefix_app_name, metric_name=BASE_HTTP_LATENCY_METRIC_NAME):
    metric_name = prefix_metric_name(metric_prefix_app_name, metric_name)
    return metric_name

def create_http_request_counter_metric_name(metric_prefix_app_name, metric_name=BASE_HTTP_COUNTER_METRIC_NAME):
    metric_name = prefix_metric_name(metric_prefix_app_name, metric_name)
    return metric_name

def create_http_request_latency_gauge_metric_name(metric_prefix_app_name, metric_name=BASE_HTTP_LATENCY_GAUGE_METRIC_NAME):
    metric_name = prefix_metric_name(metric_prefix_app_name, metric_name)
    return metric_name

def create_external_io_duration_metric_name(metric_prefix_app_name, metric_name=BASE_EXTERNAL_IO_DURATION_METRIC_NAME):
    metric_name = prefix_metric_name(metric_prefix_app_name, metric_name)
    return metric_name

def create_external_io_counter_metric_name(metric_prefix_app_name, metric_name=BASE_EXTERNAL_IO_COUNTER_METRIC_NAME):
    metric_name = prefix_metric_name(metric_prefix_app_name, metric_name)
    return metric_name

def create_external_io_exception_metric_name(metric_prefix_app_name, metric_name=BASE_EXTERNAL_IO_EXCEPTION_METRIC):
    metric_name = prefix_metric_name(metric_prefix_app_name, metric_name)
    return metric_name

def create_http_requests_exception_metric_name(metric_prefix_app_name, metric_name=BASE_HTTP_EXCEPTION_METRIC):
    metric_name = prefix_metric_name(metric_prefix_app_name, metric_name)
    return metric_name


def create_function_duration_metric_name(metric_prefix_app_name, metric_name=BASE_FUNCTION_DURATION_METRIC_NAME):
    metric_name = prefix_metric_name(metric_prefix_app_name, metric_name)
    return metric_name

def create_function_exception_metric_name(metric_prefix_app_name, metric_name=BASE_FUNCTION_EXCEPTION_METRIC):
    metric_name = prefix_metric_name(metric_prefix_app_name, metric_name)
    return metric_name

def create_http_function_latency_gauge_metric_name(metric_prefix_app_name, metric_name=BASE_FUNCTION_LATENCY_GAUGE_METRIC):
    metric_name = prefix_metric_name(metric_prefix_app_name, metric_name)
    return metric_name

def create_external_service_latency_gauge_metric_name(metric_prefix_app_name, metric_name=BASE_EXTERNAL_IO_LATENCY_GAUGE_METRIC):
    metric_name = prefix_metric_name(metric_prefix_app_name, metric_name)
    return metric_name

def create_bytes_metric_name(metric_prefix_app_name,  metric_name=BASE_BYTES_METRIC):
    metric_name = prefix_metric_name(metric_prefix_app_name, metric_name)
    return metric_name

def create_http_request_metrics(status_code, duration_ms, metric_prefix_app_name, exception_type_class=None):
    """
        Pushes duration metrics for http requests. Creates three types of metrics:
        1. Request Duration Histogram metrics
        2. Request Duration Gauge metrics(raw value in ms)
        3. Exception type counter metric is created if exception_type_class is provided and status_code is '5xx'

        Attributes:
        -----------
        status_code int: Can only be valid http status code (200, 599)
        duartion_ms float: Time taken for request in milliseconds
        metric_prefix_app_name str: This string will be added to the start of each metric generated.

        Returns tuple: (<histogram_metric_name>, <guage_metric_name>, <exception_metric_name>)
                        exception_metric_name is None is status code is other than 5xx and no exception_type_class is provided
    """
    if status_code not in HTTP_REQUEST_STATUS_CODE_OPTIONS:
        raise ValueError('status_code can only be one of {}'.format(', ',join(HTTP_REQUEST_STATUS_CODE_OPTIONS)))

    exception_metric = None
    if status_code >= 500:
        status_code = str(status_code)
        if  exception_type_class:
            exception_metric = create_http_requests_exception_metric_name(metric_prefix_app_name)
            exception_metric = add_label_to_metric_name(exception_type_class, exception_metric)
            statsd_client.incr(exception_metric)
            logger.debug('Incremented metric {}'.format(exception_metric))
    status_code = str(status_code)
    hist_request_duration = create_http_request_latency_histogram_metric(metric_prefix_app_name)
    hist_request_duration = add_label_to_metric_name(status_code, hist_request_duration)
    statsd_client.timing(hist_request_duration, duration_ms)
    logger.debug('Created histogram http metric {} with value {}'.format(hist_request_duration, duration_ms))

    request_duration_gauge_metric = create_http_request_latency_gauge_metric_name(metric_prefix_app_name)
    request_duration_gauge_metric = add_label_to_metric_name(status_code, request_duration_gauge_metric)
    statsd_client.gauge(request_duration_gauge_metric, duration_ms)
    logger.debug('Created guage http duration metric {} with value {}'.format(request_duration_gauge_metric, duration_ms))

    return hist_request_duration, request_duration_gauge_metric, exception_metric


def create_http_request_counter_metric(status_code, metric_prefix_app_name):
    """
        Increments a simple counter metric to track the number of requests made.
    """
    if status_code not in HTTP_REQUEST_STATUS_CODE_OPTIONS:
        raise ValueError('status_code can only be one of {}'.format(', ',join(HTTP_REQUEST_STATUS_CODE_OPTIONS)))

    status_code = str(status_code)
    request_counter_metric = create_http_request_counter_metric_name(metric_prefix_app_name)
    request_counter_metric = add_label_to_metric_name(status_code, request_counter_metric)
    statsd_client.incr(request_counter_metric)
    logger.debug('Created metric: request counter {}'.format(request_counter_metric))

def create_function_duration_metrics(duration_ms, metric_prefix_app_name, function_name, host, status, exception_type_class=None):
    """
        1. Pushes a Histogram based metric for functions runtime.
        2. If the status is 'error', creates a exception type counter with exception_type_class as label.
        3. It also creates a gauge based metric for function duration to capture raw function runtime values, It's always created.

        Attributes:
        -----------
        status str: can be either 'success' or 'error'
        exception_type_class str: required if status is 'error'. Name of the exception type class
    """
    if status not in FUNCTION_STATUS_VALUES:
        raise ValueError('status can only be one of [{}]'.format(', '.join(FUNCTION_STATUS_VALUES)))

    exception_metric = None

    if status == FUNCTION_STATUS_VALUES[1]:
        if not exception_type_class:
            raise ValueError('exception_type_class cannot be null if status is "error"')
        else:
            exception_metric = create_function_exception_metric_name(metric_prefix_app_name)
            exception_metric = add_label_to_metric_name(function_name, exception_metric)
            exception_metric = add_label_to_metric_name(host, exception_metric)
            exception_metric = add_label_to_metric_name(exception_type_class, exception_metric)
            statsd_client.incr(exception_metric)
            logger.debug('Incremented metric {}'.format(exception_metric))

    hist_metric = create_function_duration_metric_name(metric_prefix_app_name)
    hist_metric = add_label_to_metric_name(function_name, hist_metric)
    hist_metric = add_label_to_metric_name(host, hist_metric)
    hist_metric = add_label_to_metric_name(status, hist_metric)

    function_duration_gauge_metric = create_http_function_latency_gauge_metric_name(metric_prefix_app_name)
    function_duration_gauge_metric = add_label_to_metric_name(function_name, function_duration_gauge_metric)
    function_duration_gauge_metric = add_label_to_metric_name(host, function_duration_gauge_metric)
    function_duration_gauge_metric = add_label_to_metric_name(status, function_duration_gauge_metric)
    statsd_client.gauge(function_duration_gauge_metric, duration_ms)
    logger.debug('Created guage function duration metric {} with value {}'.format(function_duration_gauge_metric, duration_ms))
    statsd_client.timing(hist_metric, duration_ms)
    logger.debug('Pushed function duration histogram metric {} with value {}'.format(hist_metric, duration_ms))

    return hist_metric, function_duration_gauge_metric, exception_metric

def create_external_service_duration_metrics(status, duration_ms, metric_prefix_app_name, service_name, service_address, exception_type=None):
    """
        Creates metrics related to runtime of external services and exceptions raised for the same.
        Creates two metrics:
        1. Histogram based duration metric with duration in ms as the value.
        2. Counter based exception metric to count types of Exception raised during the external service call. Only created is status is 'error'.

        Attributes:
        status str: Value can only be in ['success', 'error'].
        duration_ms float: Duration for which the service ran in milliseconds.
        service_name: Name of the service which will be added as label for the metric with the same name.
        service_address: The address of the service which is being called. Added as a label with the same name.
        exception_type str: Name of the exception class raised if the status is 'error' otherwise its not required.
    """
    if status not in FUNCTION_STATUS_VALUES:
        raise ValueError('status can only be one of [{}]'.format(', '.join(FUNCTION_STATUS_VALUES)))

    exception_metric = None
    if status == FUNCTION_STATUS_VALUES[1]:
        if not exception_type:
            raise ValueError('exception_type cannot be null for status="error"')
        else:
            exception_metric = create_external_io_exception_metric_name(metric_prefix_app_name)
            exception_metric = add_label_to_metric_name(service_name, exception_metric)
            exception_metric = add_label_to_metric_name(service_address, exception_metric)
            exception_metric = add_label_to_metric_name(exception_type, exception_metric)
            statsd_client.incr(exception_metric)
            logger.debug('Incremented metric {}'.format(exception_metric))

    hist_metric = create_external_io_duration_metric_name(metric_prefix_app_name)
    hist_metric = add_label_to_metric_name(service_name, hist_metric)
    hist_metric = add_label_to_metric_name(service_address, hist_metric)
    hist_metric = add_label_to_metric_name(status, hist_metric)
    statsd_client.timing(hist_metric, duration_ms)
    logger.debug('Pushed histogram metric {} with value {}'.format(hist_metric, duration_ms))

    service_duration_gauge_metric = create_external_service_latency_gauge_metric_name(metric_prefix_app_name)
    service_duration_gauge_metric = add_label_to_metric_name(service_name, service_duration_gauge_metric)
    service_duration_gauge_metric = add_label_to_metric_name(service_address, service_duration_gauge_metric)
    service_duration_gauge_metric = add_label_to_metric_name(status, service_duration_gauge_metric)

    statsd_client.gauge(service_duration_gauge_metric, duration_ms)

    logger.debug('Created gauge external service duration metric {} with value {}'.format(service_duration_gauge_metric, duration_ms))

    return hist_metric, service_duration_gauge_metric, exception_metric

def create_bytes_metric(metric_prefix_app_name, size_in_bytes, name_label):
    """
        Function to push bytes metric.
        Attributes:
        ----------
        name_label: label to identify which component/module/function etc is being measured. <b> Cannot contain special charaters except _ .

    """
    metric_name = create_bytes_metric_name(metric_prefix_app_name)
    metric_name = add_label_to_metric_name(name_label, metric_name)

    statsd_client.gauge(metric_name, size_in_bytes)
    logger.debug('Created gauge bytes metric {} with value {}'.format(metric_name, size_in_bytes))

    return metric_name



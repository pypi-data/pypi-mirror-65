import time
import statsd
import functools
from .metrics import create_external_service_duration_metrics, create_function_duration_metrics, create_external_io_counter_metric
from .metrics import add_label_to_metric_without_mapping, logger
from .metrics import APP_NAME
from .helpers import get_hostname
from .constants import TAG_REDIS, TAG_MYSQL, TAG_API, TAG_ELASTICSEARCH, TAG_OTHER, TAG_MEMCACHE


def collect_external_io_metrics(metric_prefix_app_name, service_name, service_address=None, service_tag=TAG_OTHER):
    """
        Decorator to collect metrics from the wrapped function calling an external service. This is a lower level function if a custom tag is to be provided please use other decorators functions such as measure_api_io etc

        It returns the following metrics:
            1. service_name_external_io_duration_ms:
               Labels: name, address, tag

            2. Counter based exception metric to count types of Exception raised during the external service call. Only created if status is 'error'.
               error name will be the name of error class raised
        Attributes:
        service_address: defaults to hostname of the host running this code. Should be the address to
                         which service is pointing/calling
        service_tag: can be one of the tags defined in constants file.
    """
    if not service_address:
        service_address = get_hostname()

    def inner_func(func):
        @functools.wraps(func)
        def wrapper_decorator(*args, **kwargs):
            start_time = time.time()
            try:
                value = func(*args, **kwargs)
                end_time = time.time()
                duration_ms = (end_time - start_time)*1000
                status = 'success'

            except Exception as e:
                status = 'error'
                end_time = time.time()
                duration_ms = (end_time - start_time)*1000

                exception_type = e.__class__.__name__
                create_external_service_duration_metrics(
                    status, duration_ms, service_name, service_address, service_tag, exception_type)

                raise

            else:
                create_external_service_duration_metrics(
                    status, duration_ms, service_name, service_address, service_tag)

            finally:
                create_external_io_counter_metric(
                    service_name, service_address, service_tag)

            return value
        return wrapper_decorator
    return inner_func


def collect_function_duration_metrics(function_name, host=None):
    """
        Pushes metrics that measure function runtime as histogram and exception type counter
        It returns the following metrics:
            1. app_name_function_duration_ms.function_name.host.status:

               Here both function_name and host becomes labels
               where 'status' can be 'success' or 'error'

            2. Counter based exception metric to count types of Exception raised during the function call. Only created if status is 'error'.
               error name will be the name of error class raised

        Attributes:
        host: defaults to hostname of the host running this code
    """
    if not host:
        host = get_hostname()

    def inner_func(func):
        @functools.wraps(func)
        def wrapper_decorator(*args, **kwargs):
            start_time = time.time()
            try:
                value = func(*args, **kwargs)
                end_time = time.time()
                duration_ms = (end_time - start_time)*1000

            except Exception as e:
                status = 'error'
                end_time = time.time()
                duration_ms = (end_time - start_time)*1000
                exception_type = e.__class__.__name__
                create_function_duration_metrics(
                    duration_ms, function_name, host, status, exception_type)
                raise

            else:
                status = 'success'
                create_function_duration_metrics(
                    duration_ms, function_name, host, status)

            return value
        return wrapper_decorator
    return inner_func


def measure_redis_io(name, address=None):
    return collect_external_io_metrics(APP_NAME, name, TAG_REDIS, address)


def measure_api_io(name, address=None):
    return collect_external_io_metrics(APP_NAME, name, TAG_API, address)


def measure_memcache_io(name, address=None):
    return collect_external_io_metrics(APP_NAME, name, TAG_MEMCACHE, address)


def measure_mysql_io(name, address=None):
    return collect_external_io_metrics(APP_NAME, TAG_MYSQL, address)


def measure_elasticsearch_io(name, address=None):
    return collect_external_io_metrics(APP_NAME, name, TAG_ELASTICSEARCH, address)

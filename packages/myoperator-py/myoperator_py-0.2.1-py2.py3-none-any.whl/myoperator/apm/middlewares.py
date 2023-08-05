import time
import logging
from .metrics import  create_http_request_metrics, create_http_request_counter_metric
from django.conf import settings

def request_metrics_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        start_time_seconds = time.time()
        try:
            response = get_response(request)
            end_time_ms = ((time.time() - start_time_seconds)*1000)

            if response.status_code >= 200 and response.status_code < 300:
                status_code = '2xx'
            elif response.status_code >=300 and response.status_code < 400:
                status_code = '3xx'
            elif response.status_code >=400 and response.status_code < 500:
                status_code = '4xx'
            elif response.status_code >= 500 and response.status_code < 600:
                status_code = '5xx'

        except Exception as e:
            end_time_ms = ((time.time() - start_time_seconds)*1000)
            exception_type = e.__class__.__name__
            hist_metric_name, gauge_duration_metric_name, exception_metric_name = create_http_request_metrics('5xx', end_time_ms, settings.METRIC_APP_NAME, exception_type)
            raise

        else:
            # called when no exeptions are raised
            hist_metric_name, gauge_metric_name, exception_metric_name = create_http_request_metrics(status_code, end_time_ms, settings.METRIC_APP_NAME)

        finally:
            request_counter_metric = create_http_request_counter_metric(status_code, settings.METRIC_APP_NAME)

        return response

    return middleware

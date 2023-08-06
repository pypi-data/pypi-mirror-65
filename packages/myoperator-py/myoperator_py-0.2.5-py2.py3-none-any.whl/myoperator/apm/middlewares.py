import time
import logging
from .metrics import create_http_request_metrics, create_http_request_counter_metric
from .metrics import config_client, set_entry_point
from .constants import METRIC_APP_NAME_VAR_NAME
from .helpers import get_generic_url_from_django_route_path
from django.conf import settings

try:
   from django.core.urlresolvers import resolve
except:
    from django.urls import resolve


def request_metrics_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        start_time_seconds = time.time()
        entry_point = resolve(request.path)
        entry_point = get_generic_url_from_django_route_path(request.path, entry_point.kwargs)
        entry_point = request.method + ' ' + entry_point
        set_entry_point(entry_point)
        try:
            if hasattr(settings, METRIC_APP_NAME_VAR_NAME):
                app_name = getattr(settings, METRIC_APP_NAME_VAR_NAME)
                config_client(config_dict={
                    'app_name': app_name
                })
            response = get_response(request)
            end_time_ms = ((time.time() - start_time_seconds)*1000)
            status_code = response.status_code

        except Exception as e:
            end_time_ms = ((time.time() - start_time_seconds)*1000)
            exception_type = e.__class__.__name__
            hist_metric_name, gauge_duration_metric_name, exception_metric_name = create_http_request_metrics(
                500, end_time_ms, exception_type)
            raise

        else:
            # called when no exeptions are raised
            hist_metric_name, gauge_metric_name, exception_metric_name = create_http_request_metrics(
                status_code, end_time_ms)

        finally:
            request_counter_metric = create_http_request_counter_metric(
                status_code)

        return response

    return middleware

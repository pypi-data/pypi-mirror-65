import unittest
from time import sleep
import os
import random
import requests
import statsd
from datetime import datetime, timezone, timedelta
from myoperator.apm.decorators import collect_external_io_metrics, collect_function_duration_metrics
from myoperator.apm.metrics import create_external_io_duration_metric_name
from myoperator.apm.metrics import create_function_duration_metric_name
from myoperator.apm.metrics import config_client, create_external_service_duration_metrics
from myoperator.apm.metrics import create_function_duration_metrics, create_http_request_metrics

PROMETHEUS_API_URL = os.environ.get('PROMETHEUS_API_URL', 'http://localhost:9090/api/v1/query')
METRIC_PREFIX = 'myoperator'

def get_prometheus_data(params):
    return requests.get(PROMETHEUS_API_URL,
                params = params
            )

class TestApmClientFunctions(unittest.TestCase):

    def test_create_function_duration_metrics(self):
        status_code = '2xx'
        create_function_duration_metrics(200, METRIC_PREFIX, 'TEST_FUNCTION', 'test_host', 'success')
        # invalid input
        self.assertRaises(ValueError, create_function_duration_metrics, 200, METRIC_PREFIX, 'TEST_FUNCTION', 'test_host', 'wrong_status')

    def test_create_http_request_metrics(self):
        status_code = '2xx'
        duration_ms = 300
        create_http_request_metrics(status_code, duration_ms, METRIC_PREFIX)

        exception_type = type(ValueError('Test Error')).__name__
        create_http_request_metrics('5xx', duration_ms, METRIC_PREFIX, exception_type)

        # wrong status
        self.assertRaises(ValueError, create_http_request_metrics, 200, duration_ms, METRIC_PREFIX,)

    def test_create_external_service_duration_metric(self):
        status = 'error'
        exception_class = type(RuntimeError('Test Runtime Error')).__name__
        create_external_service_duration_metrics(status, 100, METRIC_PREFIX, 'test_service', 'test_service_address', exception_class)
        create_external_service_duration_metrics('success', 100, METRIC_PREFIX, 'test_service', 'test_service_address')

        # no exception class provided
        self.assertRaises(ValueError, create_external_service_duration_metrics, status, 100, METRIC_PREFIX, 'test_service', 'test_service_address')
        self.assertRaises(ValueError, create_external_service_duration_metrics, 'wrong_status', 100, METRIC_PREFIX, 'test_service', 'test_service_address')


class TestConfigClient(unittest.TestCase):

    def test_config_client(self):
        from myoperator.apm.metrics import statsd_client
        self.assertTrue(isinstance(statsd_client, statsd.StatsClient))
        config_client('UDP')

        self.assertTrue(isinstance(statsd_client, statsd.StatsClient))

        config_client('TCP')
        from myoperator.apm.metrics import statsd_client
        self.assertTrue(isinstance(statsd_client, statsd.TCPStatsClient))

class TestDecorators(unittest.TestCase):

    def test_collect_external_io_metrics(self):
        class TestException(Exception):
            pass

        @collect_external_io_metrics(METRIC_PREFIX, service_name='test_service')
        def dummy_func():
            raise TestException('Error')

        try:
            dummy_func()
        except TestException:
            pass

        @collect_external_io_metrics(METRIC_PREFIX, service_name='test_service')
        def dummy_func():
            pass

        dummy_func()

    def test_collect_function_metrics_decorator(self):
        class TestException(Exception):
            pass

        @collect_function_duration_metrics(METRIC_PREFIX, function_name='test_dummy_func')
        def dummy_func():
            raise TestException('Error')

        try:
            dummy_func()
        except TestException:
            pass

        @collect_function_duration_metrics(METRIC_PREFIX, function_name='test_dummy_func')
        def dummy_func():
            pass

        dummy_func()

class TestIntegrationDecorators(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        config_client('TCP')
        pass

    def test_collect_external_io_metrics_decrator(self):
        @collect_external_io_metrics(METRIC_PREFIX, service_name='test_service')
        def dummy_func():
            choice = [True, False]
            sel_choice = random.choice(choice)
            if sel_choice:
                raise RuntimeError('Error')
            sleep(1)

        dt = datetime.now()
        start_time = dt.replace(tzinfo=timezone.utc).timestamp()
        try:
            dummy_func()
            sleep(1)
        except RuntimeError:
            pass

        end_time = (dt + timedelta(seconds=1)).replace(tzinfo=timezone.utc).timestamp()
        expected_metric_name = create_external_io_duration_metric_name(METRIC_PREFIX) + '_count'
        response = get_prometheus_data({
                'query': expected_metric_name ,
                'start': start_time,
                'end': end_time
            })

        data = response.json()
        self.assertTrue(response.ok)
        self.assertTrue(data['data']['result'])

        result = data['data']['result']
        for item in result:
            self.assertEqual(item['metric']['service_name'], 'test_service')

    def test_collect_external_io_metrics_decrator_tcp(self):
        config_client('TCP')

        @collect_external_io_metrics(METRIC_PREFIX, service_name='test_service')
        def dummy_func():
            choice = [True, False]
            sel_choice = random.choice(choice)
            if sel_choice:
                raise RuntimeError('Error')
            sleep(1)

        dt = datetime.now()
        start_time = dt.replace(tzinfo=timezone.utc).timestamp()
        try:
            dummy_func()
            sleep(1)
        except RuntimeError:
            pass

        end_time = (dt + timedelta(seconds=1)).replace(tzinfo=timezone.utc).timestamp()
        expected_metric_name = create_external_io_duration_metric_name(METRIC_PREFIX) + '_count'
        response = get_prometheus_data({
                'query': expected_metric_name ,
                'start': start_time,
                'end': end_time
            })

        config_client('UDP')

        data = response.json()
        self.assertTrue(response.ok)
        self.assertTrue(data['data']['result'])

        result = data['data']['result']
        for item in result:
            self.assertEqual(item['metric']['service_name'], 'test_service')

    def test_collect_function_metrics_decorator(self):
        @collect_function_duration_metrics(METRIC_PREFIX, function_name='test_dummy_func')
        def dummy_func():
            choice = [True, False]
            sel_choice = random.choice(choice)
            if sel_choice:
                raise RuntimeError('Error')
            sleep(1)

        dt = datetime.now()
        start_time = dt.replace(tzinfo=timezone.utc).timestamp()
        try:
            dummy_func()
        except RuntimeError:
            pass

        end_time = (dt + timedelta(seconds=0.1)).replace(tzinfo=timezone.utc).timestamp()
        expected_metric_name = create_external_io_duration_metric_name(METRIC_PREFIX) + '_count'
        response = get_prometheus_data({
                'query': expected_metric_name ,
                'start': start_time,
                'end': end_time
            })

        data = response.json()
        self.assertTrue(response.ok)
        self.assertTrue(data['data']['result'])

        result = data['data']['result']
        for item in result:
            self.assertEqual(item['metric']['service_name'], 'test_service')


if __name__ == '__main__':
    unittest.main()


import unittest
from metrics import create_bytes_metric

class TestLibraryFunctions(unittest.TestCase):

    def test_create_bytes_metric(self):
        create_bytes_metric('myoperator', 2064, 'test_bytes')


if __name__ == '__main__':
    unittest.main()

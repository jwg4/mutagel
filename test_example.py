import unittest

import example

class TestFibonacci(unittest.TestCase):
    def test_basic_case(self):
        self.assertEqual(example.fibonacci(1), 0)
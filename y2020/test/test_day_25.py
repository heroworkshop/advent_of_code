import unittest

from y2020.day_25 import parse


class TestDay25(unittest.TestCase):
    def test_parse(self):
        result = parse("231")
        self.assertEqual(231, result)
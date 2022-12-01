import unittest

from day_02 import make_numpad_keys


class TestDay02(unittest.TestCase):
    def test_make_numpad_keys(self):
        PAD = "123\n456\n789"
        pad, start = make_numpad_keys(PAD)
        self.assertEqual((1,1), start)

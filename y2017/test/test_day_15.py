import unittest

from y2017.day_15 import compare_loword


class TestDay15(unittest.TestCase):
    def test_compare_loword_withEqualBottom16Bits_returnsTrue(self):
        a = 245556042
        b = 1431495498
        self.assertTrue(compare_loword(a, b))

    def test_compare_loword_withDifferentBottom16Bits_returnsFalse(self):
        a = 1181022009
        b = 1233683848
        self.assertFalse(compare_loword(a, b))

if __name__ == '__main__':
    unittest.main()

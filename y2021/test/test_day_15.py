import unittest

from y2021.day_15 import cap_val


class TestMakeBigGrid(unittest.TestCase):
    def test_cap_val(self):
        self.assertEqual(1, cap_val(1))
        self.assertEqual(9, cap_val(9))
        self.assertEqual(1, cap_val(10))


if __name__ == '__main__':
    unittest.main()

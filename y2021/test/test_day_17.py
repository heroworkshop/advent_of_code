import unittest

class TestRangeFinding(unittest.TestCase):
    def test_is_in_range(self):
        self.assertFalse(is_in_range(171, -60, x_range, y_range))

if __name__ == '__main__':
    unittest.main()

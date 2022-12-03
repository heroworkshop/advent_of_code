import unittest

from y2016.day_14 import make_stretched_hash


class TestDay14(unittest.TestCase):
    def test_stretched_hash(self):
        result = make_stretched_hash(0, "abc")
        self.assertEqual("a107ff634856bb300138cac6568c0f24", result)


if __name__ == '__main__':
    unittest.main()

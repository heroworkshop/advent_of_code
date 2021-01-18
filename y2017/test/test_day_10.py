import unittest

from y2017.day_10 import dense_hash, CircularBuffer


class TestDay10(unittest.TestCase):
    def test_dense(self):
        expected = [64 for _ in range(16)]
        in_str = "65 ^ 27 ^ 9 ^ 1 ^ 4 ^ 3 ^ 40 ^ 50 ^ 91 ^ 7 ^ 6 ^ 0 ^ 2 ^ 5 ^ 68 ^ 22"
        seq = [int(n) for n in in_str.split(" ^ ")]
        values = []
        for _ in range(16):
            values.extend(seq)
        buffer = CircularBuffer(256)
        buffer.values = values
        result = dense_hash(buffer)
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()

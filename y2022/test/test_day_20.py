import unittest

from assertpy import assert_that

from y2022.day_20 import CircularBuffer


class TestMix(unittest.TestCase):
    def test_mix_example(self):
        entries = [1, 2, -3, 3, -2, 0, 4]
        buffer = CircularBuffer(entries)
        buffer.mix()
        result = sum(buffer.grove_coordinates())
        assert_that(result).is_equal_to(3)

    def test_grove_coordinates(self):
        entries = [3, -2, 1, 2, -3, 4, 0]
        buffer = CircularBuffer(entries)
        result = buffer.grove_coordinates()
        assert_that(result).is_equal_to([4, -3, 2])

    def test_mix_withDuplicates(self):
        entries = [1, -2, -3, -3, -2, 0, 4]
        buffer = CircularBuffer(entries)
        buffer.mix()
        assert_that(buffer.ordered()).is_equal_to( [4, 0, -2, 1, -2, -3, -3])

    def test_mix_withBigNumbersMultipleOfLength(self):
        entries = [7, 14, 28, -7, -14, 0, -28]
        buffer = CircularBuffer(entries)
        buffer.mix()
        assert_that(buffer.ordered()).is_equal_to( [7, 14, 28, -7, -14, 0, -28])

    def test_mix_big_numbers(self):
        entries = [8, 16, 30, -9, -15, 0, -29]
        buffer = CircularBuffer(entries)
        buffer.mix()
        assert_that(buffer.ordered()).is_equal_to([-9, 8, 16, -15, 30, -29, 0])


if __name__ == '__main__':
    unittest.main()

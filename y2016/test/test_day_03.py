import unittest

from day_03 import solution2, extract_as_column_groups, convert_from_text

SIMPLE_GROUP = [[1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]]


class TestDay02(unittest.TestCase):
    def test_solution2_withNoValidTriangles(self):
        input_data = SIMPLE_GROUP
        count = solution2(input_data)
        self.assertEqual(0, count)

    def test_solution2_withSomeValidTriangles(self):
        input_data = [
            [10, 6, 3],
            [4, 12, 6],
            [7, 8, 9]
        ]
        count = solution2(input_data)
        self.assertEqual(2, count)

    def test_extract_as_column_groups(self):
        input_data = SIMPLE_GROUP
        expected = [
            [1, 4, 7],
            [2, 5, 8],
            [3, 6, 9]
        ]
        triangles = extract_as_column_groups(input_data)
        self.assertEqual(expected, triangles)


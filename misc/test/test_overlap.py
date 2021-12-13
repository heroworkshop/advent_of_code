import unittest

from misc.overlap import Circles, overlaps, Circle


class TestOverlap(unittest.TestCase):
    def test_overlaps_withOverlappingCircles_returnsTrue(self):
        circles = [((0, 0, 1), (0, 1.5, 1)),
                   ((100, 100, 8), (110, 110, 8)),
                   ((-50, 0, 50), (0, 50, 100)),
                   ]
        for c1, c2 in circles:
            self.assertTrue(overlaps(Circle(*c1), Circle(*c2)))

    def test_overlaps_withNonOverlappingCircles_returnsFalse(self):
        circles = [((0, 0, 1), (0, 2.5, 1)),
                   ((100, 100, 7), (110, 110, 7)),
                   ((-50, 0, 50), (0, 50, 10)),
                   ]
        for c1, c2 in circles:
            self.assertFalse(overlaps(Circle(*c1), Circle(*c2)))

    def test_find_largest_group_OneOverlap(self):
        circles = Circles([(50, 50, 10), (61, 50, 2), (161, 161, 2)])
        result = circles.find_largest_group()
        self.assertEqual(2, len(result))
        self.assertEqual(1, min(result) + 1)

    def test_find_largest_group_100CirclesAllOverlapping(self):
        circles = Circles([(x, 0, 10) for x in range(0, 1500, 15)])
        result = circles.find_largest_group()
        self.assertEqual(100, len(result))
        self.assertEqual(1, min(result) + 1)

    def test_find_largest_group_with2Groups_picksLargestGroup(self):
        group1 = [(x, 0, 10) for x in range(0, 1515, 15)]
        group2 = [(x, 100, 10) for x in range(0, 1500, 15)]
        circles = Circles([*group1, *group2])
        result = circles.find_largest_group()
        self.assertEqual(101, len(result))
        self.assertEqual(1, min(result) + 1)


if __name__ == '__main__':
    unittest.main()

import unittest

from y2021.day_19 import ROTATIONS, manhatten_distance


class TestDay19(unittest.TestCase):
    def test_rotations(self):
        results = {rot(1, 2, 3) for rot in ROTATIONS}
        expected = {(1, 2, 3), (-2, 1, 3), (-1, -2, 3), (2, -1, 3), (-3, 2, 1), (-2, -3, 1), (3, -2, 1), (2, 3, 1),
                    (-1, 2, -3), (-2, -1, -3), (1, -2, -3), (2, 1, -3), (3, 2, -1), (-2, 3, -1), (-3, -2, -1),
                    (2, -3, -1), (1, -3, 2), (3, 1, 2), (-1, 3, 2), (-3, -1, 2), (1, 3, -2), (-3, 1, -2), (-1, -3, -2),
                    (3, -1, -2)}
        self.assertEqual(expected, results)

    def test_manhatten_distance(self):
        p1, p2 = (1105, -1205, 1229), (-92, -2380, -20)
        result = manhatten_distance(p1, p2)
        self.assertEqual(3621, result)

if __name__ == '__main__':
    unittest.main()

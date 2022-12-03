import unittest

from y2021.day_22 import Cuboid, solution2


class TestCuboid(unittest.TestCase):
    def test_count_overlaps(self):
        a = Cuboid((0, 0, 0), (10, 10, 10))
        b = Cuboid((5, 5, 5), (6, 6, 6))
        result = a.count_overlaps(b)
        self.assertEqual(8, result)

    def test_subtract_withHalfOverlap_returnsHalfOfCuboid(self):
        a = Cuboid((0, 0, 0), (10, 10, 10))
        b = Cuboid((5, 0, 0), (10, 10, 10))
        result = a.subtract(b)
        self.assertEqual(1, len(result))

    def test_subtract_withCornerOverlap_returnsRemainder(self):
        a = Cuboid((0, 0, 0), (10, 10, 10))
        b = Cuboid((5, 0, 0), (15, 5, 5))
        result = a.subtract(b)
        self.assertEqual(3, len(result))

    def test_volume_with3x3x3Cube_hasVolume27(self):
        volume = Cuboid((10, 10, 10), (13, 13, 13)).volume

        self.assertEqual(27, volume)


class TestSolution2(unittest.TestCase):
    def test_solution_add2Cubes(self):
        lines = [
            (True, ((0, 0), (0, 0), (0, 0))),
            (True, ((1, 1), (0, 0), (0, 0)))
        ]
        volume = solution2(lines)
        self.assertEqual(2, volume)

    def test_solution_add2OverlappingCubes(self):
        lines = [
            (True, ((0, 1), (0, 1), (0, 1))),
            (True, ((1, 1), (0, 0), (0, 0)))
        ]
        volume = solution2(lines)
        self.assertEqual(8, volume)

    def test_solution_subtract2OverlappingCubes(self):
        lines = [
            (True, ((0, 1), (0, 1), (0, 1))),
            (False, ((1, 1), (0, 0), (0, 0)))
        ]
        volume = solution2(lines)
        self.assertEqual(7, volume)

    def test_solution_add2CornerOverlappingCubes(self):
        lines = [
            (True, ((0, 1), (0, 1), (0, 1))),
            (True, ((1, 2), (1, 2), (1, 2)))
        ]
        volume = solution2(lines)
        self.assertEqual(15, volume)

    def test_solution_subtract2CornerOverlappingCubes(self):
        lines = [
            (True, ((0, 1), (0, 1), (0, 1))),
            (False, ((1, 2), (1, 2), (1, 2)))
        ]
        volume = solution2(lines)
        self.assertEqual(7, volume)

    def test_solution_subtract2NegativeCornerOverlappingCubes(self):
        lines = [
            (True, ((-1, 0), (-1, 0), (-1, 0))),
            (False, ((-2, -1), (-2, -1), (-2, -1)))
        ]
        volume = solution2(lines)
        self.assertEqual(7, volume)


if __name__ == '__main__':
    unittest.main()

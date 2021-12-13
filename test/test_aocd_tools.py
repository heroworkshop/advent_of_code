import unittest

from aocd_tools import Grid, grid_from_lines, int_tuples_from_lines, ints_from_lines


class TestParsingFunctions(unittest.TestCase):
    def test_int_tuples_from_lines(self):
        lines = """
        1, 2, 3
        4, 5, 6
        """
        result = int_tuples_from_lines(lines, ",")
        self.assertEqual([(1, 2, 3), (4, 5, 6)], result)

    def test_ints_from_lines(self):
        lines = """
        1
        4
        3
        """
        result = ints_from_lines(lines)
        self.assertEqual([1, 4, 3], result)


class TestGrid(unittest.TestCase):
    def test_bounds(self):
        grid = Grid()
        grid.add((-1, -2), "#")
        grid.add((5, 10), "#")
        grid.update_bounds()
        self.assertEqual(-1, grid.x_bounds.min)
        self.assertEqual(-2, grid.y_bounds.min)
        self.assertEqual(5, grid.x_bounds.max)
        self.assertEqual(10, grid.y_bounds.max)

    def test_linear_index(self):
        grid = Grid()
        grid.add((0,0), ".")
        grid.add((1,1), ".")
        grid.update_bounds()
        self.assertEqual(0, grid.linear_index((0, 0)))
        self.assertEqual(1, grid.linear_index((1, 0)))
        self.assertEqual(2, grid.linear_index((0, 1)))
        self.assertEqual(3, grid.linear_index((1, 1)))




class TestGridFromLines(unittest.TestCase):
    def test_grid_from_lines(self):
        lines = ("aaa\n"
                 "bbb\n"
                 "ccc\n")

        grid = grid_from_lines(lines)
        self.assertEqual(0, grid.x_bounds.min)
        self.assertEqual(2, grid.x_bounds.max)
        self.assertEqual(0, grid.y_bounds.min)
        self.assertEqual(2, grid.x_bounds.max)

        self.assertEqual("a", grid.at((0, 0)))


if __name__ == '__main__':
    unittest.main()

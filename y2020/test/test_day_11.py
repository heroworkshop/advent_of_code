import unittest
from aocd_tools import grid_from_lines
from y2020.day_11 import count_neighbours, count_visible_neighbours

M1 = """
###
###
###""".strip()

M2 = """
##.
##.
.##""".strip()

M3 = """
.............
.L.L.#.#.#.#.
.............
""".strip()

class TestNeighbours(unittest.TestCase):
    def test_count_neighbours_withSurroundedCell(self):
        grid = grid_from_lines(M1)
        result = count_neighbours(grid.grid, (1, 1), "#")
        self.assertEqual(8, result)

    def test_count_neighbours_withPartiallySurroundedCell(self):
        grid = grid_from_lines(M2)
        result = count_neighbours(grid.grid, (1, 1), "#")
        self.assertEqual(5, result)

    def test_count_visible_neighbours_withHiddenSeats(self):
        grid = grid_from_lines(M3)
        result = count_visible_neighbours(grid.grid, (1, 1), "#")
        self.assertEqual(0, result)

    def test_count_visible_neighbours_withOneVisibleSeat(self):
        grid = grid_from_lines(M3)
        result = count_visible_neighbours(grid.grid, (1, 1), "L")
        self.assertEqual(1, result)

if __name__ == '__main__':
    unittest.main()

import unittest

from aocd_tools import grid_from_lines
from y2020.day_20 import make_edges, rotate_tile, points_from_lines, count_overlapping_shapes, points_from_grid

M2311 = """
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###
""".strip()

M3079 = """
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
""".strip()

M3079CW90 = """
...#.##..#
....###.#.
####.###.#
...#.##...
#.##..#.##
#.#####.##
#.##....##
....#...##
...###..##
...#....#.
""".strip()

M3079FLIPPED = """
..#.###...
..#.......
..#.###...
#.#####.##
.#...#.##.
####.#..#.
######....
..#.......
.#..######
#.#.#####.
""".strip()

SHAPE = """
######
####
""".strip()


class TestDay20(unittest.TestCase):

    def test_points_from_grid(self):
        expected = set([
            (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5,0),
            (0, 1), (1, 1), (2, 1), (3, 1),
        ])
        grid = grid_from_lines(SHAPE)
        points = points_from_grid(grid.grid)
        self.assertEqual(expected, points)

    def test_count_overlapping_shapes_withPixels(self):
        shape_points = [(0, 0)]
        grid = grid_from_lines("## ##", )
        count, points = count_overlapping_shapes(grid.grid, [shape_points], width=5, height=1)
        self.assertEqual(4, count)

    def test_count_overlapping_shapes_withSquares(self):
        shape_points = [(0, 0), (1, 0), (0, 1), (1, 1)]
        grid = grid_from_lines("#####\n#####", )
        count, points = count_overlapping_shapes(grid.grid, [shape_points], width=5, height=2)
        self.assertEqual(2, count)

    def test_count_overlapping_shapes_withNoRotations(self):
        shape_points = [points_from_lines(SHAPE)]
        grid = grid_from_lines(M3079FLIPPED)
        count, points = count_overlapping_shapes(grid.grid, shape_points, width=grid.width, height=10)
        self.assertEqual(1, count)

    def test_count_overlapping_shapes_withSimpleGridAllRotations(self):
        shape_grid = grid_from_lines(("##\n"
                                      "#"))
        shape_grids = [rotate_tile(shape_grid.grid, n, width=2, height=2) for n in range(8)]
        shape_points = [points_from_grid(sg) for sg in shape_grids]
        grid = grid_from_lines("## # \n"
                               "#  ##")
        count, points = count_overlapping_shapes(grid.grid, shape_points, width=grid.width, height=2)
        self.assertEqual(2, count)

    def test_count_overlapping_shapes_withAllRotations(self):
        shape_grid = grid_from_lines(SHAPE)
        shape_grids = [rotate_tile(shape_grid.grid, n, 6, 2) for n in range(8)]
        shape_points = [points_from_grid(sg) for sg in shape_grids]
        grid = grid_from_lines(M3079FLIPPED)
        count, points = count_overlapping_shapes(grid.grid, shape_points, width=grid.width, height=10)
        self.assertEqual(2, count)

    def test_rotate_tile_withRot0_returnsUnchanged(self):
        grid = grid_from_lines(M3079)
        expected = grid.grid
        result = rotate_tile(grid.grid, 0, 10, 10)
        self.assertEqual(expected, result)

    def test_rotate_tile_withRot1_returnsRotatedCW90(self):
        grid = grid_from_lines(M3079)
        expected = grid_from_lines(M3079CW90).grid
        result = rotate_tile(grid.grid, 1, 10, 10)
        self.assertEqual(expected, result)

    def test_rotate_tile_withRot4_returnsFlipped(self):
        grid = grid_from_lines(M3079)
        expected = grid_from_lines(M3079FLIPPED).grid
        result = rotate_tile(grid.grid, 4, 10, 10)
        self.assertEqual(expected, result)

    def test_make_edges_withFirstRotation_hasCorrectEdgeValues(self):
        grid = grid_from_lines(M2311)
        edges = make_edges(grid.grid)
        self.assertEqual(210, edges[0][0])
        self.assertEqual(89, edges[0][1])
        self.assertEqual(231, edges[0][2])
        self.assertEqual(498, edges[0][3])

    def test_make_edges_withFirstRotation_hasCorrectTop(self):
        grid = grid_from_lines(M2311)
        edges = make_edges(grid.grid)
        self.assertEqual(318, edges[1][0])

    def test_make_edges_withSecondRotation_hasCorrectEdges(self):
        grid = grid_from_lines(M2311)
        edges = make_edges(grid.grid)
        self.assertEqual(924, edges[2][0])
        self.assertEqual(318, edges[2][1])
        self.assertEqual(616, edges[2][3])

        grid = grid_from_lines(M3079)
        edges = make_edges(grid.grid)
        self.assertEqual(616, edges[0][3])

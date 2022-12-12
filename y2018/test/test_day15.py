from unittest import TestCase
from assertpy import assert_that

from aocd_tools import grid_from_lines
from y2018.day_15 import extract_actors, move_actor, nearest_enemy

LAYOUT_E3G = """#######
                #E..G.#
                #...#.#
                #.G.#G#
                #######"""


def make_grid(s):
    lines = [line.strip() for line in s.split("\n")]
    return grid_from_lines("\n".join(lines))


class TestParsing(TestCase):
    def test_extract_actors(self):
        grid = make_grid(LAYOUT_E3G)
        actors = extract_actors(grid)
        assert_that(actors).is_length(4)
        assert_that(actors[(1, 1)].symbol).is_equal_to("E")
        assert_that(actors[(4, 1)].symbol).is_equal_to("G")
        assert_that(actors[(2, 3)].symbol).is_equal_to("G")
        assert_that(actors[(5, 3)].symbol).is_equal_to("G")


class TestMove(TestCase):
    def setUp(self):
        self.grid = make_grid(LAYOUT_E3G)
        self.actors = extract_actors(self.grid)

    def test_move_actor(self):
        move_actor((1, 1), (2, 1), self.actors, self.grid)
        assert_that((1, 1)).is_not_in(self.actors)
        assert_that(self.actors[(2, 1)].symbol).is_equal_to("E")
        assert_that(self.grid.at((1, 1))).is_equal_to(".")
        assert_that(self.grid.at((2, 1))).is_equal_to("E")

    def test_nearest_enemy(self):
        pos = nearest_enemy(self.actors[(1, 1)], self.actors, self.grid)
        assert_that(pos).is_equal_to((4, 1))

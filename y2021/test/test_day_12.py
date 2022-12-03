import unittest
from aocd_tools import grid_from_lines
from y2021.day_12 import can_follow_route, Cave


class TestAddRoute(unittest.TestCase):
    def test_add_small_cave_withCaveAlreadyOnRoute_returnsTrue(self):
        cave = Cave("b")
        result = can_follow_route(["start", "A", "b", "A"], cave)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()

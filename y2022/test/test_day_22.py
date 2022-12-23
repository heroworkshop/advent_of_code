import unittest

from assertpy import assert_that

from aocd_tools import Pos
from y2022.day_22 import Player, make_grid, make_edges, RIGHT, DOWN, LEFT, UP, show_path


class TestTransformEdges(unittest.TestCase):
    def setUp(self):
        self.grid, _ = make_grid(BIG_MAP)
        self.edges = make_edges()

    def test_bf(self):
        start_pos = Pos(50, 0)
        directions = ["L", 2]
        player = Player(start_pos, self.edges)
        player.play(self.grid, directions)
        assert_that(player.pos).is_equal_to((1, 150))
        assert_that(player.direction).is_equal_to(RIGHT)

    def test_fb(self):
        start_pos = Pos(0, 155)
        directions = ["L", "L", 2]
        player = Player(start_pos, self.edges)
        player.play(self.grid, directions)
        assert_that(player.pos).is_equal_to((55, 1))
        assert_that(player.direction).is_equal_to(DOWN)

    def test_ac(self):
        start_pos = Pos(101, 49)
        directions = ["R", 2]
        player = Player(start_pos, self.edges)
        player.play(self.grid, directions)
        assert_that(player.pos).is_equal_to((98, 51))
        assert_that(player.direction).is_equal_to(LEFT)

    def test_ca(self):
        start_pos = Pos(97, 55)
        directions = [4]
        player = Player(start_pos, self.edges)
        player.play(self.grid, directions)
        # show_path(self.grid, player)
        assert_that(player.pos).is_equal_to((105, 48))
        assert_that(player.direction).is_equal_to(UP)

    def test_af(self):
        start_pos = Pos(106, 2)
        directions = ["L", 4]
        player = Player(start_pos, self.edges)
        player.play(self.grid, directions)
        show_path(self.grid, player)
        assert_that(player.pos).is_equal_to((6, 198))
        assert_that(player.direction).is_equal_to(UP)

    def test_af_with_wall(self):
        start_pos = Pos(118, 2)
        directions = ["L", 4]
        player = Player(start_pos, self.edges)
        player.play(self.grid, directions)
        show_path(self.grid, player)
        assert_that(player.pos).is_equal_to((118, 0))
        assert_that(player.direction).is_equal_to(UP)

    def test_fa(self):
        start_pos = Pos(48, 198)
        directions = ["R", 4]
        player = Player(start_pos, self.edges)
        player.play(self.grid, directions)
        show_path(self.grid, player)
        assert_that(player.pos).is_equal_to((148, 2))
        assert_that(player.direction).is_equal_to(DOWN)

    def test_da(self):
        start_pos = Pos(98, 102)
        directions = ["L", "R", 4]
        player = Player(start_pos, self.edges)
        player.play(self.grid, directions)
        show_path(self.grid, player)
        assert_that(player.pos).is_equal_to((147, 47))
        assert_that(player.direction).is_equal_to(LEFT)

    def test_ad(self):
        start_pos = Pos(148, 2)
        directions = ["L", "R", 4]
        player = Player(start_pos, self.edges)
        player.play(self.grid, directions)
        show_path(self.grid, player)
        assert_that(player.pos).is_equal_to((97, 147))
        assert_that(player.direction).is_equal_to(LEFT)

    def test_ce(self):
        start_pos = Pos(51, 57)
        directions = ["L", "L", 4]
        player = Player(start_pos, self.edges)
        player.play(self.grid, directions)
        show_path(self.grid, player)
        assert_that(player.pos).is_equal_to((7, 102))
        assert_that(player.direction).is_equal_to(DOWN)

    def test_ec(self):
        start_pos = Pos(2, 101)
        directions = ["L", 4]
        player = Player(start_pos, self.edges)
        player.play(self.grid, directions)
        show_path(self.grid, player)
        assert_that(player.pos).is_equal_to((52, 52))
        assert_that(player.direction).is_equal_to(RIGHT)

    def test_be(self):
        start_pos = Pos(51, 1)
        directions = ["L", "L", 4]
        player = Player(start_pos, self.edges)
        player.play(self.grid, directions)
        show_path(self.grid, player)
        assert_that(player.pos).is_equal_to((2, 148))
        assert_that(player.direction).is_equal_to(RIGHT)

    def test_eb(self):
        start_pos = Pos(1, 101)
        directions = ["L", "L", 4]
        player = Player(start_pos, self.edges)
        player.play(self.grid, directions)
        show_path(self.grid, player)
        assert_that(player.pos).is_equal_to((52, 48))
        assert_that(player.direction).is_equal_to(RIGHT)


BIG_MAP = """                                                  ..#......#........................#...#......#.............#...........#......#...#............#....
                                                  ......#..........#...........#....................#....................................#..#.........
                                                  ...............#.##.............##...#..#..#.......#.#............#.#.#...#..................#......
                                                  ...............................#..#........................#......#...#............#................
                                                  .#....#.......#....#.......#.............#..#...........#.............#............#........#.......
                                                  ........#..................#.#........#......#.......#............#....##.........#.........#..#....
                                                  #.........................##..............##...................#.....##..............#..............
                                                  #............................................#..........#......#.#..........#...........#....#......
                                                  ..........................#.#.....#......#.....#...................................#.....#......#...
                                                  .....#...........##.....................................................##.#...#....................
                                                  .....#....#.#....................#.#....#.................#.........#.#................#...#........
                                                  #..........#.#.........#....#...........................................##......#...........#......#
                                                  .........#..##......#.....#...........#....##.....#........#..##....#................#..............
                                                  .....#..........##...........#................#.......#......#..............#......#.......#........
                                                  ........#......##......#..........#......#...................................#......................
                                                  ......................#..#........................................#.......#..........#.....#........
                                                  .#...#......#......#...................#....#..##...............##...#........#......#..............
                                                  .##...#.#....#.......##.......................#...........#...........#....#.#.........##........#..
                                                  ...#......................#.#...#............#......#............#....#.......#.............##......
                                                  .......................#..................#....#.....#.......#..............................#.......
                                                  #............#......#......#.#.....#.............#......#..............#.........#.......#....#..#..
                                                  ............................##.........#..........#......#......#.............#..................#..
                                                  ..............#..#.....#..#................#..#.................##.....#...........#.....#...#.##...
                                                  ...#..#...#.........###.........#....................................#......#....#.................#
                                                  ................#.......#.........#.........................#......#.........##.......#......#.#....
                                                  ...#........#....#.....................#.................#.#......#.........#.......#....#..##...#.#
                                                  .....#.....#.....#........#.....................#..#....#..............#...............#.........#..
                                                  ................#.............##.#.#..#..#.#..........#......#...#.#..............#...#..#..........
                                                  .......###......#..#......#........#.........................#......##........#.#.......#..##.#.....
                                                  .#.......#................#................#.....##..............................#...#..............
                                                  #...........................#...........#....##..........................#...........#.........#....
                                                  .....................................#..........#.................#.#...........#..................#
                                                  ....#...#.##.............#..#................................#.............#.......##...............
                                                  ......##............#...#....#.........#...............#.......#............#..........#........##..
                                                  ..#...#.................#.............#..#................#..........#.......#......................
                                                  ......#..........................#...#.......##..#..#...........................#....#.#......#.....
                                                  ...##........#.............#.#.......#...................#............##.........#.....#............
                                                  ...........#...................#.#.................#..............#.........#........##..#.....##...
                                                  .........#.....#.#......................................#.............#..............#....#.........
                                                  ...##.#.......#..#.......#........##..........#.............................#....#.........#.....#..
                                                  #.........#..........#......##......#.......#.........................#....#.....##............#....
                                                  ...#.#.#.......#.....#......#.............#......#.#............#....#.................#............
                                                  .........#......#......#..#....#.#.#..#.....#.....#......##.....#...#.#..................##..#.##...
                                                  .......#......#........#...#.........#..#..........#..................#.............#.......#.......
                                                  ......................#.......#................#......#.##.......##...........#....#........##......
                                                  ..#........#..#.....................##.................#...##....#..................#...###.....#...
                                                  .#...........................#........#......................#.......#..............................
                                                  ....................#..#...#....#...........#.............................#.....................#...
                                                  .....#.....#.....................#...#.#....................................#....#....###.......#.#.
                                                  ....................#.....#......#................#........##...............#.......................
                                                  ...............#.#.............#.....#.#......#...
                                                  .........#...#.#.#................................
                                                  ........................#..............#..........
                                                  .....#........#......................#.##.....##..
                                                  #................#.........................#.....#
                                                  .#....#.............#.......#....#.#......#.......
                                                  ...#........#...........#.....#...........#......#
                                                  ...#............#........#......#............###..
                                                  .#.........#...#..............#.#.......#.........
                                                  .....#...........................#........#......#
                                                  ..........#.....#....#.##.............#...#.......
                                                  .###....##................#..............##......#
                                                  ......#.#..........#...................#........#.
                                                  ....................##...........#................
                                                  ........#..........##.............................
                                                  .....#.#.................#...........#.....#......
                                                  ....#.................#...........................
                                                  ..................................#...............
                                                  .....#.......#............#......#..#....###..#...
                                                  .#....#.....................................#.....
                                                  ..##........................#...........#.#.......
                                                  .......#.......#.#................#......#........
                                                  .................#.#....#.............#.##........
                                                  ...#.............................#.........#......
                                                  ..#........#...............#..................#...
                                                  ..............................#......#............
                                                  .#..........##.#..............#.........#....#..#.
                                                  ..#............##..........#..#..........#......#.
                                                  .....#.......#......#......................#......
                                                  .............................##.............#.....
                                                  ..............................#...................
                                                  ....#......#.#..........#......#.........#..#.....
                                                  ........#.....#....#..##.#.#.#....................
                                                  ...............##......................#.......##.
                                                  .......#..............#........#.......#...#....#.
                                                  ......#.............#...#..#.#.......#.##.....#...
                                                  .................#....#..#..............#.........
                                                  ...#......#....#.....#.......#........#...#.#..#..
                                                  .........#....#.....#.............##..............
                                                  ......................#...........................
                                                  ......#...#.........#.............................
                                                  ......#.#......................................#..
                                                  ....#..........#................#....#.#.#........
                                                  .........#.................##.......#.......#.....
                                                  ............#....#...#...............##....#.#...#
                                                  ....................................#.............
                                                  #..#..#...........#.................#.#...........
                                                  ....#.......................#........#.#...#......
                                                  #............#.......................#........#...
                                                  .........#......#.......#.#..............#.##....#
....#...........#....#.............................#.......#........#.#.#..##....#.##......#......#.
...#..........................#.##.#.............................#.................###.#............
...........#.......#.#..................................#............................#.#........#...
....#..............#.#......#.#.#.#...#.......................#.............#............#....#.#...
.............#....#..............#..#......#..........#...................#....#......#......#......
..#...........#..#.......#.............#...........................#....#.#..#............#.........
.................#.......#.#..............##....................................##.#................
.....##..#...#...#....#................#.#....#..................#..................................
....#............#...........#.#.................#.....................#....................#...#...
............................#...#..............##..#....#....#.....#..........#.....................
.......#.......#.#......##.........#................#.#..#..#.................#.....................
..#...........................##.............#...................................#...#.#............
..#..........................#.##.......#...............##.......................#.......#...#......
...................#..#.......................#...##.........................#..................#...
...##..........#......................#.#...............#.#.....#.#...............................#.
................................#...........##.....#.....#.........#.........#...........#..#..#....
..............................#....#.....#............#................#.##..................#..#.##
.....................#.#......#.....#...#.....##.............#......#.#.............................
.....##.................#.......#.................#.##............#..........#..#.....#..#..........
#..#................#..........#.........#..#....................#......#..........#..........#.....
............#..............##................#.#...#........##.........#......#..#......#......#....
....##....................#.........................#....##...............#...###.....#.............
.......#..............#...........##..####.....#.....#.####...........###......#....................
......#....#...##...........#.....#.................#.....##.....#......#.........##................
....#................................................#.........#..........................#..#.##...
##...#..........................#...#.............#.......................#.#..#.........###..#...#.
#...........#.#.....................#...............#.............#..#.......#......................
....#..#.......................#...#..........#......#.#.....#..................................#...
...............................#...#..............#..#..#..........#.........................#......
....#.......................#.........#........................................#.............#......
....................#...........#..........#.....#......#..........#............#.........#.....#...
.....#...#..........#...............#..#............#...##.................#...............##.......
.........................#.................................#........................#.....#..#......
...........#.#..#........#.#....##........#...#.........................#.#.........................
...............#.......#..#...#....#.......................#......................................#.
.........##..#......#..##...#............#..#.....#......##..............................#..........
.............................#.#.#...................#............#....#.........#..##....#.........
........#.......#.....#..........#.................................#........................#....#..
#.......#.........#...........#...........................#.##.#..........#....#.##.....#.........#.
.....#..........#..........#...##................#..........#....................#.....#..#.#......#
.........................#..#..........#...#.......#..............#.#..#.#...#...#..................
...###.....#.#...............#........................................#.#.#...#.#........#...#......
......#.........#.........................#......#.....##..............#........##...#..............
...........#.........#...........#..#...#....#..................#.#....#........#...#.....#.........
......##...#...............#..................................#.#........#....##.##.#...............
....#..#..................................#..#....#....................................#..#.#.......
.....#.................#.#....#...#.#.....................#.......................................#.
.#..#.#.........#.........#..............##.#....#..#.#......##............##..........#........#...
...........#.....#.......#..#.................................#............#........................
...#.#.....#........#................#.#.....#.....................#...#............#..##...........
....##..............#..............###..##........
............##........##..........................
.#.#.......#...................#..................
....#..................................#....#.....
#.......#..#...#....#..#..#.............#.........
........#...#.................#...........#.......
.#...#..........#.........#.............##........
.......#...................#........#........#....
#......##..#.............#....#.#.#.........#.....
....................#..#..........................
...#.......#........#....#.............#.#.....#.#
.#..............#...#........#....#...............
.........................#....#...##.......#......
...#.............#..#..........#.#.#....#...#.....
.#...............#...#...#....#.......#...........
...#............................##............#...
...#...........................#...........#..#...
..#......#...........#...#...........##...#..#....
........#.......................#..........#....#.
...............#..............#......#.......##...
..........#.....#.......#.....#...........#.#.....
#...#....#......#..#........#.........##......#.#.
.....##....#..........#.......#...................
#...#.....................................#......#
....#....#..#...#....#..............#..#..........
............##...........#...#....................
........#........#....#........#...........#......
..#..#....................#..............#...#....
...............#..........#.##....................
.#.....#......#...................................
.....................................#............
...#......#....................#.........#.......#
..........#..........#..........#....#............
.....................#.....#..............##......
................#..............#......#....#......
.......#....#.##..##..#..............#...#.....#..
.....#.......##...............#........#.......#..
.......#...........#..............................
.#..........#...........................###.#..#..
...#......#..#..............#.....................
...........##....#..............##......##........
............#.#........................#.#.#....#.
........#..............#.................#........
.......#....................##....#............#..
..#.##..............#......#............#.........
##..#...........#..#....#.....#...........#.#.....
.#.#.......#...#..#.............#.................
......................................#.....#.....
.....#.#.........#................................
..................#........#........#.##..........
"""

if __name__ == '__main__':
    unittest.main()

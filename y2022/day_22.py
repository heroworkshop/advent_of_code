from collections import deque
from dataclasses import dataclass
from typing import NamedTuple, List, Tuple, Dict, Union

from aocd_tools import load_input_data, Grid, Pos

EXAMPLE = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""


def parse_directions(directions_str):
    directions = []
    buffer = ""
    for ch in directions_str:
        if ch in "RL":
            if buffer:
                directions.append(int(buffer))
                buffer = ""
            directions.append(ch)
        else:
            buffer += ch
    if buffer:
        directions.append(int(buffer))
    return directions


def run(observer=None):
    input_data = load_input_data(2022, 22)
    # input_data = EXAMPLE

    print(f"loaded input data ({len(input_data)} bytes)")

    map_str, directions_str = input_data.split("\n\n")
    grid, start_pos = make_grid(map_str)
    directions = parse_directions(directions_str)
    print(grid.render())
    print(f"{grid.width} by {grid.height} grid")
    print(directions)

    print("solution1 = ", solution1(grid, start_pos, directions, observer))
    grid, start_pos = make_grid(map_str)
    print("solution2 = ", solution2(grid, start_pos, directions))


def make_grid(s) -> Grid:
    grid = Grid()
    start_pos = None
    for y, row in enumerate(s.split("\n")):
        for x, ch in enumerate(row):
            if ch == "." and start_pos is None:
                start_pos = x, y
            grid.add((x, y), ch)
    grid.update_bounds()
    return grid, start_pos


DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
DIR_CH = [">", "v", "<", "^"]

UP = 3
DOWN = 1
RIGHT = 0
LEFT = 2


def ac(p: Pos) -> Tuple[Pos, int]:
    return Pos(99, p.x - 50), LEFT


def ca(p: Pos) -> Tuple[Pos, int]:
    return Pos(p.y + 50, 49), UP


def ce(p: Pos) -> Tuple[Pos, int]:
    return Pos(p.y - 50, 100), DOWN


def ec(p: Pos) -> Tuple[Pos, int]:
    return Pos(50, p.x + 50), RIGHT


def fd(p: Pos) -> Tuple[Pos, int]:
    return Pos(p.y - 100, 149), UP


def df(p: Pos) -> Tuple[Pos, int]:
    return Pos(49, p.x + 100), LEFT


def be(p: Pos) -> Tuple[Pos, int]:
    return Pos(0, 149 - p.y), RIGHT


def eb(p: Pos) -> Tuple[Pos, int]:
    return Pos(50, 149 - p.y), RIGHT


def da(p: Pos) -> Tuple[Pos, int]:
    return Pos(149, 149 - p.y), LEFT


def ad(p: Pos) -> Tuple[Pos, int]:
    return Pos(99, 149 - p.y), LEFT


def fb(p: Pos) -> Tuple[Pos, int]:
    return Pos(p.y - 100, 0), DOWN


def bf(p: Pos) -> Tuple[Pos, int]:
    return Pos(0, p.x + 100), RIGHT


def af(p: Pos) -> Tuple[Pos, int]:
    return Pos(p.x - 100, 199), UP


def fa(p: Pos) -> Tuple[Pos, int]:
    return Pos(p.x + 100, 0), DOWN


def make_edges():
    edges = {}
    # AC
    for x in range(100, 150):
        edges[(Pos(x, 49), DOWN)] = ac
    # CA
    for y in range(50, 100):
        edges[(Pos(99, y), RIGHT)] = ca
    # CE
    for y in range(50, 100):
        edges[(Pos(50, y), LEFT)] = ce
    # EC
    for x in range(0, 50):
        edges[(Pos(x, 100), UP)] = ec
    # FD
    for y in range(150, 200):
        edges[(Pos(49, y), RIGHT)] = fd
    # DF
    for x in range(50, 100):
        edges[(Pos(x, 149), DOWN)] = df
    # FB
    for y in range(150, 200):
        edges[(Pos(0, y), LEFT)] = fb
    # BF
    for x in range(50, 100):
        edges[(Pos(x, 0), UP)] = bf
    # BE
    for y in range(0, 50):
        edges[(Pos(50, y), LEFT)] = be
    # EB
    for y in range(100, 150):
        edges[(Pos(0, y), LEFT)] = eb
    # DA
    for y in range(100, 150):
        edges[(Pos(99, y), RIGHT)] = da
    # AD
    for y in range(0, 50):
        edges[(Pos(149, y), RIGHT)] = ad
    # AF
    for x in range(100, 150):
        edges[(Pos(x, 0), UP)] = af
    # FA
    for x in range(0, 50):
        edges[(Pos(x, 199), DOWN)] = fa
    return edges


class Player:
    def __init__(self, start_pos: Pos, edges=None, observer=None):
        self.edges = edges or {}
        self.pos = start_pos
        self.direction = 0
        self.path = {}
        self.observer = observer

    def play(self, grid: Grid, directions: List[Union[str, int]]):
        for d in directions:
            if d == "R":
                self.direction = (self.direction + 1) % 4
                # print("turn right", self.direction)
            elif d == "L":
                self.direction = (self.direction - 1) % 4
                # print("turn left", self.direction)
            else:
                self.move_forward(d, grid, self.edges)
            dir_ch = DIR_CH[self.direction]
            self.path[self.pos] = dir_ch
            if self.observer:
                self.observer.update(self, grid)

    def move_forward(self, d: int, grid: Grid, edges: Dict):
        # print(f"take {d} steps")
        while d:
            new_direction = self.direction
            if (self.pos, self.direction) in edges:
                transform = edges[(self.pos, self.direction)]
                p, new_direction = transform(self.pos)
                # print(f"warping to {p}")
            else:
                v = Pos(*DIRECTIONS[self.direction])
                p = v + Pos(*self.pos)
                x, y = p
                x = x % grid.width
                y = y % grid.height
                p = Pos(x, y)
                if self.at(p, grid) == " ":
                    p = self.wrap(p, grid)
                    # print(f"Wrapping to {p}")
            if self.at(p, grid) == "#":
                # print("    hit wall")
                break

            self.pos = p
            self.direction = new_direction
            dir_ch = DIR_CH[self.direction]
            self.path[self.pos] = dir_ch
            d -= 1
        # print(f"    now at {self.pos}")

    def at(self, p: Pos, grid: Grid) -> str:
        return " " if p not in grid.grid else grid.at(p)

    def wrap(self, p: Pos, grid: Grid):
        x, y = p
        if self.direction == 0:
            x = 0
            while grid.at((x, y)) == " ":
                x += 1
        elif self.direction == 1:
            y = 0
            while grid.at((x, y)) == " ":
                y += 1
        elif self.direction == 2:
            x = grid.width - 1
            while grid.at((x, y)) == " ":
                x -= 1
        elif self.direction == 3:
            y = grid.height
            while grid.at((x, y)) == " ":
                y -= 1
        return Pos(x, y)


def solution1(grid, start_pos, directions, observer=None):  # < 93242
    player = Player(start_pos, observer=observer)
    player.play(grid, directions)

    for p, ch in player.path.items():
        grid.add(p, ch)

    print(grid.render())

    return 1000 * (player.pos.y + 1) + 4 * (player.pos.x + 1) + player.direction


def solution2(grid, start_pos, directions):  # < 90288
    edges = make_edges()
    player = Player(start_pos, edges)
    player.play(grid, directions)

    show_path(grid, player)

    return 1000 * (player.pos.y + 1) + 4 * (player.pos.x + 1) + player.direction


def show_path(grid, player):
    for p, ch in player.path.items():
        grid.add(p, ch)
    print(grid.render())


if __name__ == "__main__":
    run()

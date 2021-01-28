# If you get this error:
#     "Puzzle inputs differ by user.  Please log in to get your puzzle input."
# Then you need to import the session cookie
#
# For getting session cookie see:
# https://github.com/wimglenn/advent-of-code-wim/issues/1
#
# Login on AoC with github or whatever Open browser's developer console (e.g. right click --> Inspect) and navigate
# to the Network tab GET any input page, say adventofcode.com/2016/day/1/input, and look in the request headers. It's
# a long hex string. Export that to an environment variable AOC_SESSION. Or, if you prefer more persistence,
# you can write it to a plain text file at ~/.config/aocd/token.
#

import io
from collections import defaultdict, namedtuple

from aocd.models import Puzzle


def load_input_data(year, day):
    return Puzzle(year=year, day=day).input_data


def ints_from_lines(lines):
    return [int(line) for line in lines.split("\n")]


def int_tuples_from_lines(lines, sep):
    result = []
    for line in lines.split("\n"):
        result.append(tuple([int(i) for i in line.split(sep)]))
    return result


def compute_bounds(values, border=1):
    Boundary = namedtuple("boundary", "min max")
    return Boundary(min(values) - border, max(values) + border)


class Grid:
    def __init__(self, border=0, default_val=" "):
        self.grid = defaultdict(lambda: default_val)
        self.x_bounds = None
        self.y_bounds = None
        self.border = border

    @property
    def width(self):
        return self.x_bounds.max - self.x_bounds.min + 1

    def linear_index(self, p):
        return p[0] + p[1] * self.width

    def update_bounds(self):
        self.x_bounds = compute_bounds([p[0] for p in self.grid], border=self.border)
        self.y_bounds = compute_bounds([p[1] for p in self.grid], border=self.border)

    def add(self, p, ch):
        self.grid[p] = ch

    def at(self, p):
        return self.grid[p]

    def render(self) -> str:
        result = io.StringIO()
        for y in range(self.y_bounds.min, self.y_bounds.max + 1):
            for x in range(self.x_bounds.min, self.x_bounds.max + 1):
                ch = self.grid[(x, y)]
                print(ch, file=result, end="")
            print(file=result)
        return result.getvalue()


def grid_from_lines(lines: str) -> Grid:
    result = Grid()
    x, y = 0, 0
    for line in lines.split("\n"):
        for ch in line:
            result.add((x, y), ch)
            x += 1
        x, y = 0, y + 1
    result.update_bounds()
    return result


class Grid4d(Grid):
    def __init__(self, default_val=" "):
        super().__init__(default_val=default_val)
        self.z_bounds = None
        self.w_bounds = None

    def update_bounds(self):
        super().update_bounds()
        self.z_bounds = compute_bounds([p[2] for p in self.grid], border=self.border)
        self.w_bounds = compute_bounds([p[2] for p in self.grid], border=self.border)

    def render(self, z=0, w=0, empty=".") -> str:
        result = io.StringIO()
        for y in range(self.y_bounds.min, self.y_bounds.max + 1):
            for x in range(self.x_bounds.min, self.x_bounds.max + 1):
                p = (x, y, z, w)
                if p in self.grid():
                    ch = self.grid[(x, y, z, w)]
                else:
                    ch = empty
                print(ch, file=result, end="")
            print(file=result)
        return result.getvalue()


def grid4d_from_lines(lines: str, z=0, w=0, default_val=" ") -> Grid4d:
    result = Grid4d(default_val=default_val)
    x, y = 0, 0
    for line in lines.split("\n"):
        for ch in line:
            if ch != default_val:
                result.add((x, y, z, w), ch)
            x += 1
        x, y = 0, y + 1
    result.update_bounds()
    return result

# If you get this error:
#     "Puzzle inputs differ by user.  Please log in to get your puzzle input."
# Then you need to import the session cookie
#
from aocd.exceptions import DeadTokenError

AOCD_COOKIE_HELP = """
For getting session cookie see:
https://github.com/wimglenn/advent-of-code-wim/issues/1

Login on AoC with google authentication or whatever Open browser's developer console (e.g. right click --> Inspect) and navigate
to the Network tab GET any input page, say adventofcode.com/2016/day/1/input, and look in the request headers. It's
a long hex string. For example click on "input" and look for the "cookie:" section and take the value after "session=".
Export that to an environment variable AOC_SESSION. Or, if you prefer more persistence,
you can write it to a plain text file at ~/.config/aocd/token.
"""

import inspect
import io

from collections import defaultdict, namedtuple
from pathlib import Path

from aocd.models import Puzzle


def load_input_data(year=None, day=None):
    f = inspect.currentframe()
    calling_fname = f.f_back.f_code.co_filename
    year = year or int(Path(calling_fname).parent.stem[1:])
    day = day or int(Path(calling_fname).stem[4:6])
    print(f"Advent of Code {year}, day {day}")
    try:
        return Puzzle(year=year, day=day).input_data
    except DeadTokenError as e:
        print(AOCD_COOKIE_HELP)
        raise e

def ints_from_lines(lines, sep="\n"):
    return [int(line) for line in lines.split(sep) if line.strip()]


def int_tuples_from_lines(lines, sep):
    return [tuple([int(i) for i in line.strip().split(sep) if i])
            for line in lines.strip().split("\n")
            if line
           ]


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

    @property
    def x_vals(self):
        return range(self.x_bounds.min, self.x_bounds.max)

    @property
    def y_vals(self):
        return range(self.y_bounds.min, self.y_bounds.max)

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
        self.update_bounds()
        result = io.StringIO()
        for y in range(self.y_bounds.min, self.y_bounds.max + 1):
            for x in range(self.x_bounds.min, self.x_bounds.max + 1):
                ch = self.grid[(x, y)]
                print(ch, file=result, end="")
            print(file=result)
        return result.getvalue()

    def all_neighbours(self, p):
        x, y = p
        return [
            (x+dx, y+dy)
            for dx, dy in [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
            if (x+dx, y+dy) in self.grid
        ]


def grid_from_lines(lines: str, default_val=" ", transform=lambda x: x) -> Grid:
    result = Grid(default_val=default_val)
    x, y = 0, 0
    for line in lines.split("\n"):
        for ch in line:
            if ch != default_val:
                result.add((x, y), transform(ch))
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

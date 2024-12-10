# If you get this error:
#     "Puzzle inputs differ by user.  Please log in to get your puzzle input."
# Then you need to import the session cookie
#
import time
from typing import NamedTuple

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

from collections import namedtuple
from pathlib import Path

from aocd.models import Puzzle


class Pos(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Pos(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Pos(self.x - other.x, self.y - other.y)


class Pos3d(NamedTuple):
    x: int
    y: int
    z: int

    def __add__(self, other):
        return Pos3d(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Pos3d(self.x - other.x, self.y - other.y, self.z - other.z)


ALL_DIRECTIONS = [Pos(*p) for p in ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1))]
NEIGHBOURS = [p for p in ALL_DIRECTIONS if not all(p)]


def get_elapsed(start_t):
    t = time.process_time() - start_t
    if t < 1:
        return f"{t * 1000:.3} ms"
    if t > 120:
        return f"{t / 60:.3} mins"
    return f"{t:.3} s"


def load_input_data(year=None, day=None):
    if not year or not day:
        f = inspect.currentframe()
        calling_fname = f.f_back.f_code.co_filename
        year = year or int(Path(calling_fname).parent.stem[1:])
        day = day or int(Path(calling_fname).stem[4:6])
    print(f"Advent of Code {year}, day {day}", flush=True)
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
        self.grid = {}
        self.x_bounds = None
        self.y_bounds = None
        self.border = border
        self.default_val = default_val

    def in_bounds(self, pos: Pos):
        if pos.x < self.x_bounds.min:
            return False
        if pos.x > self.x_bounds.max:
            return False
        if pos.y < self.y_bounds.min:
            return False
        if pos.y > self.y_bounds.max:
            return False
        return True

    @property
    def width(self):
        return self.x_bounds.max - self.x_bounds.min + 1

    @property
    def height(self):
        return self.y_bounds.max - self.y_bounds.min + 1

    @property
    def x_vals(self):
        return range(self.x_bounds.min, self.x_bounds.max + 1)

    @property
    def y_vals(self):
        return range(self.y_bounds.min, self.y_bounds.max + 1)

    def linear_index(self, p):
        return p[0] + p[1] * self.width

    def update_bounds(self):
        self.x_bounds = compute_bounds([p[0] for p in self.grid], border=self.border)
        self.y_bounds = compute_bounds([p[1] for p in self.grid], border=self.border)

    def add(self, p, ch):
        self.grid[p] = ch

    def at(self, p):
        return self.grid.get(p, self.default_val)

    def render(self, overlay=None) -> str:
        self.update_bounds()
        result = io.StringIO()
        for y in range(self.y_bounds.min, self.y_bounds.max + 1):
            for x in range(self.x_bounds.min, self.x_bounds.max + 1):
                if overlay and (x, y) in overlay:
                    ch = overlay[(x, y)]
                else:
                    ch = self.grid.get((x, y), self.default_val)
                print(ch, file=result, end="")
            print(file=result)
        return result.getvalue()

    def all_neighbours(self, p):
        x, y = p
        return [
            (x + dx, y + dy)
            for dx, dy in NEIGHBOURS
            if (x + dx, y + dy) in self.grid
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


def time_report(start_time) -> str:
    end_time = time.process_time()
    diff = end_time - start_time
    if diff > 3600:
        h = int(diff // 3600)
        m = int((diff % 3600) // 60)
        return f"{h}h {m}m"
    if diff > 60:
        m = int(diff // 60)
        s = diff % 60
        return f"{m}m {s}s"
    return f"{diff}s"

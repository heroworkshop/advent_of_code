from collections import deque
from dataclasses import dataclass
from typing import NamedTuple, List

from aocd_tools import load_input_data, Grid

EXAMPLE = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""


class Point(NamedTuple):
    x: int
    y: int


def make_point(s: str):
    parts = s.split(",")
    return Point(*[int(p) for p in parts])


def make_grid(points: List[List[Point]]) -> Grid:
    grid = Grid()
    grid.add((500, 0), "+")
    for section in points:
        start = None
        end = None
        for p in section:
            start = end
            end = p
            if start:
                if start.y != end.y:
                    draw_vertical(start, end, grid)
                else:
                    draw_horizontal(start, end, grid)
    return grid


def draw_vertical(start, end, grid):
    #print(f"draw vertical from {start} to {end}")
    r = range(start.y, end.y + 1) if start.y < end.y else range(end.y, start.y + 1)
    for y in r:
        grid.add((start.x, y), "#")
        #print(f"{start.x, y} ", end="")
    #print()


def draw_horizontal(start, end, grid):
    #print(f"draw horisontal from {start} to {end}")
    r = range(start.x, end.x + 1) if start.x < end.x else range(end.x, start.x + 1)
    for x in r:
        grid.add((x, start.y), "#")
        #print(f"{x, start.y} ", end="")
    #print()


def show(grid):
    for y in grid.y_vals:
        for x in grid.x_vals:
            ch = grid.at((x, y)) if (x, y) in grid.grid else "."
            print(ch, end="")
        print()
    print()


def run():
    input_data = load_input_data(2022, 14)
    # input_data = EXAMPLE

    print(f"loaded input data ({len(input_data)} bytes)")

    entries = input_data.split("\n")
    entries = [parse(line) for line in entries]
    print(entries[:50])

    print("solution1 = ", solution1(entries))

    print("solution2 = ", solution2(entries))


def parse(line: str):
    points = line.split(" -> ")
    return [make_point(s) for s in points]


def solution1(entries):
    grid = make_grid(entries)
    grid.update_bounds()
    show(grid)
    n = 0
    try:
        while True:
            add_sand(Point(500, 1), grid)
            n += 1
    except BoundsError:
        pass
    show(grid)
    return n


def solution2(entries):
    grid = make_grid(entries)
    grid.update_bounds()
    add_floor(grid)
    grid.update_bounds()
    show(grid)
    del grid.grid[(500, 0)]
    n = 0
    try:
        while True:
            add_sand(Point(500, 0), grid)
            n += 1
            if n % 10000 == 0:
                show(grid)
    except BoundsError:
        pass
    show(grid)
    return n + 1


def add_floor(grid):
    y = grid.y_bounds.max + 2
    x1 = grid.x_bounds.min - 200
    x2 = grid.x_bounds.max + 200
    for x in range(x1, x2):
        grid.add((x, y), "#")


class BoundsError(ValueError):
    pass


def add_sand(p, grid):
    def try_falling(dx, dy):
        if (p.x + dx, p.y + dy) not in grid.grid or (p.x + dx, p.y + dy) == (500, 0):
            return Point(p.x + dx, p.y + dy)
        return None
    while True:
        if p.y > grid.y_bounds.max:
            raise BoundsError
        for d in [(0, 1), (-1, 1), (1, 1)]:
            if (p_next := try_falling(*d)) is not None:
                p = p_next
                break
        else:
            grid.add(p, "o")
            if p == (500, 0):
                raise BoundsError
            return


if __name__ == "__main__":
    run()

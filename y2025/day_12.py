from pprint import pprint
from typing import NamedTuple

from aocd_tools import Grid, Boundary
from y2025.day12_data import DATA

EXAMPLE = """
0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
""".strip()

def parse(data):
    parts = [
            line.strip().split("\n")
        for line in data.strip().split("\n\n")
    ]
    tiles = [make_tile(x[1:]) for x in parts[:-1]]
    areas = [make_area(x) for x in parts[-1]]
    return tiles, areas


def make_tile(tile_str: list[str]):
    tile = set()
    for y, s in enumerate(tile_str):
        for x, ch in enumerate(s):
            if ch == "#":
                tile.add((x, y))
    return tile

class Area(NamedTuple):
    width: int
    height: int
    indexes: list[int]


def make_area(s: str):
    dims, indexes = s.split(": ")
    width, height = map(int, dims.split("x"))
    indexes = list(map(int, indexes.split()))
    return Area(width, height, indexes)

def part1():
    result = 0
    base_types, areas = parse(DATA)
    pprint(base_types)
    print("-"*30)
    pprint(areas)

    tile_types = make_rotated_tiles(base_types)
    draw_tiles(tile_types)

    for area in areas:
        grid = Grid(default_val=".")
        grid.x_bounds = Boundary(min=0, max=area.width)
        grid.y_bounds = Boundary(min=0, max=area.height)

        # place_tiles(tile_types, grid, area.indexes)
        if sum(area.indexes) *7 <= area.width * area.height:
            result += 1

    return result


def draw_tiles(tile_types):
    rot = 0
    while rot <4:
        for y in range(4):
            for ttype in tile_types[rot]:
                for x in range(4):
                    print("#" if (x,y) in ttype else ".", end="")
                print(" ", end="")
            print()
        print()
        rot += 1

def make_rotated_tiles(tile_types):
    rotated_tiles = []
    for tile_type in tile_types:
        row = [tile_type]
        for _ in range(3):
            tile_type = rotated(tile_type)
            row.append(tile_type)
        rotated_tiles.append(row)
    return rotated_tiles

def rotated(tile):
    return {(y, 2-x) for x, y in tile}

def place_tiles(tile_types: list[set], grid: Grid):
    queue = []


def part2():
    result = 0
    return result


if __name__ == "__main__":
    print("part1:", part1())
    print("part2:", part2())

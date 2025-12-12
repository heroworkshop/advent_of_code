from pprint import pprint
from typing import NamedTuple

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
    blocks = [make_block(x) for x in parts[:-1]]
    areas = [make_area(x) for x in parts[-1]]
    return blocks, areas


def make_block(x: list[str]):
    block = set()
    for y, s in enumerate(x):
        for x, ch in enumerate(s):
            if ch == "#":
                block.add((x, y))
    return block

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
    blocks, areas = parse(EXAMPLE)
    pprint(blocks)
    print("-"*30)
    pprint(areas)

    return result


def part2():
    result = 0
    return result


if __name__ == "__main__":
    print("part1:", part1())
    print("part2:", part2())

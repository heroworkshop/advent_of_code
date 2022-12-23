from collections import deque
from dataclasses import dataclass
from typing import NamedTuple, List, Tuple, Dict, Set

from aocd_tools import load_input_data, Grid, Pos

EXAMPLE = """
..............
..............
.......#......
.....###.#....
...#...#.#....
....#...##....
...#.###......
...##.#.##....
....#..#......
..............
..............
.............."""


EX0 = """
.....
..##.
..#..
.....
..##.
....."""

def run():
    input_data = load_input_data(2022, 23)
    # input_data = EXAMPLE

    print(f"loaded input data ({len(input_data)} bytes)")

    grid = make_grid(input_data)
    print(grid.render())

    print("solution1 = ", solution1(grid))

    grid = make_grid(input_data)
    print("solution2 = ", solution2(grid))


def make_grid(s) -> Grid:
    grid = Grid(default_val=".")
    for y, row in enumerate(s.split("\n")):
        for x, ch in enumerate(row):
            if ch == "#":
                grid.add((x, y), ch)
    grid.update_bounds()
    return grid


SECTORS = [
    [(0, -1), (-1, -1), (1, -1)],  # N
    [(0, 1), (-1, 1), (1, 1)],  # S
    [(-1, 0), (-1, -1), (-1, 1)],  # W
    [(1, 0), (1, -1), (1, 1)],  # E
]

def sector_empty(sector: List, p: Pos, grid: Grid):
    for d in sector:
        dp = Pos(*d)
        prop = p + dp
        if grid.at(prop) == "#":
            return False
    return True

def propose(p: Pos, grid: Grid, proposed: Dict, start_sector):
    for i in range(4):
        sector_id = (i + start_sector) % len(SECTORS)
        sector = SECTORS[sector_id]
        if sector_empty(sector, p, grid):
            dp = Pos(*sector[0])
            prop = p + dp
            if prop not in grid.grid:
                if prop in proposed:
                    proposed[prop].append(p)
                else:
                    proposed[prop] = [p]
                return


def is_stationary(p: Pos, grid: Grid):
    count = sum(not sector_empty(SECTORS[i], p, grid) for i in range(4))
    return count in (0, 4)


def solution1(grid: Grid):
    initial_elves = len(grid.grid)
    print(f"{initial_elves} Elves")
    for start_sector in range(10):
        proposed = {}
        stationary = set()
        for p in grid.grid:
            p = Pos(*p)
            if is_stationary(p, grid):
                stationary.add(p)
            else:
                propose(p, grid, proposed, start_sector)
        new_grid = Grid(default_val=".")
        stationary_count = 0
        move_count = 0
        block_count = 0
        for p, from_p in proposed.items():
            if len(from_p) == 1:
                move_count += 1
                new_grid.add(p, "#")
            else:
                for p_blocked in from_p:
                    block_count += 1
                    new_grid.add(p_blocked, "#")
        for p in stationary:
            stationary_count += 1
            new_grid.add(p, "#")
        print(f"{stationary_count} stationary elves")
        print(f"{block_count} blocked elves")
        print(f"{move_count} moving elves")
        grid = new_grid
        print(f"== end of round {start_sector + 1} ==")
        assert len(grid.grid) == initial_elves
        print(grid.render())
    grid.update_bounds()
    size = grid.width * grid.height
    occupied = len(grid.grid)
    return size - occupied


def solution2(grid: Grid):
    initial_elves = len(grid.grid)
    print(f"{initial_elves} Elves")
    start_sector = 0
    while True:
        proposed = {}
        stationary = set()
        for p in grid.grid:
            p = Pos(*p)
            if is_stationary(p, grid):
                stationary.add(p)
            else:
                propose(p, grid, proposed, start_sector)
        new_grid = Grid(default_val=".")
        stationary_count = 0
        move_count = 0
        block_count = 0
        for p, from_p in proposed.items():
            if len(from_p) == 1:
                move_count += 1
                new_grid.add(p, "#")
            else:
                for p_blocked in from_p:
                    block_count += 1
                    new_grid.add(p_blocked, "#")
        for p in stationary:
            stationary_count += 1
            new_grid.add(p, "#")
        # print(f"{start_sector + 1}")
        if stationary_count == initial_elves:
            return start_sector + 1
        grid = new_grid
        assert len(grid.grid) == initial_elves
        start_sector += 1

if __name__ == "__main__":
    run()

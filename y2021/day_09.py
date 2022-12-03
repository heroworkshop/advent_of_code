from collections import deque
from functools import reduce

from aocd_tools import load_input_data, grid_from_lines


EXAMPLE ="""2199943210
3987894921
9856789892
8767896789
9899965678"""

def parse(line):
    return int(line)


def run():
    input_data = load_input_data()
    # input_data  = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    # lines = [parse(line) for line in input_data.split("\n")]
    grid = grid_from_lines(input_data, transform=int)
    print("solution1 = ", solution1(grid))
    print("solution2 = ", solution2(grid))


def solution1(grid):
    print(grid.render())
    grid.update_bounds()

    low_points = []
    for y in range(grid.y_bounds.min, grid.y_bounds.max + 1):
        for x in range(grid.x_bounds.min, grid.x_bounds.max + 1):
            adj_vals = [grid.at(neighbour)
                        for neighbour in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
                        if neighbour in grid.grid]
            val = grid.at((x, y))
            if min(adj_vals) > val:
                low_points.append(val + 1)
    return sum(low_points)


def solution2(grid):
    basin_sizes = []
    done = set()
    for p, height in grid.grid.items():
        if height != 9 and p not in done:
            basin = find_basin(p, grid)
            for bp in basin:
                done.add(bp)
            basin_sizes.append(len(basin))

    return reduce(lambda a, b: a*b, sorted(basin_sizes)[-3:])


def find_basin(at_point, grid):
    basin = set()
    to_do = deque([at_point])
    while to_do:
        p = to_do.pop()
        if p not in basin:
            basin.add(p)
            x, y = p
            for neighbour in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                if neighbour not in basin and neighbour in grid.grid and grid.at(neighbour) != 9:
                    to_do.append(neighbour)
    return basin


if __name__ == "__main__":
    run()

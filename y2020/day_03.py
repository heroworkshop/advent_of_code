from collections import namedtuple
from functools import reduce

from aocd_tools import load_input_data, ints_from_lines, grid_from_lines

EXAMPLE = """
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#""".strip()

def make_entry(line):
    return line


def run():
    input_data = load_input_data(2020, 3)
    # input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")

    grid = grid_from_lines(input_data)

    print("solution1 = ", solution1(grid, slope = (3, 1)))
    print("solution2 = ", solution2(grid))


def solution1(grid, slope):
    x, y = 0, 0

    count = 0
    print("width=", grid.width)
    while y < grid.y_bounds.max:
        y += slope[1]
        x += slope[0]
        x = x % grid.width
        if grid.at((x, y)) == "#":
            count += 1

    # print(grid.render())
    return count


def solution2(grid):
    slopes = (
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2)
    )
    counts = [solution1(grid, c) for c in slopes]
    return reduce(lambda a, b: a * b, counts, 1)


if __name__ == "__main__":
    run()

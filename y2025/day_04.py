from aocd_tools import grid_from_lines, Grid, Pos
from y2025.day04_data import DATA

EXAMPLE = """
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
""".strip()

def parse(data):
    lines = [line.strip() for line in data.strip().split("\n")]
    return lines


def part1():
    grid = grid_from_lines(DATA, ".")
    print(grid)
    result = 0
    for pos in grid.grid:
        n = count_surrounding(grid, pos)
        if n < 4:
            result += 1

    return result



def count_surrounding(grid: Grid, pos: Pos) -> int:
    return sum(1
               for nx, ny in grid.all_surrounding(pos)
               if (nx, ny) in grid.grid
               )


def part2():
    grid = grid_from_lines(DATA, ".")
    result = 0
    while True:
        remove = set()
        for pos in grid.grid:
            n = count_surrounding(grid, pos)
            if n < 4:
                result += 1
                remove.add(pos)
        grid.grid = {p: x for p, x in grid.grid.items() if p not in remove}
        if not remove:
            break

    return result


if __name__ == "__main__":
    print("part1:", part1())
    print("part2:", part2())

import re
from aocd_tools import *

EXAMPLE = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""


def run():
    input_data = load_input_data(2024, 6)
    # input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    # entries = int_tuples_from_lines(lines=input_data, sep=" ")
    grid = grid_from_lines(input_data, ".")

    print(grid.render())
    pos, direction = guard_pos(grid)

    for i, f in enumerate((solution1, solution2), 1):
        start_time = time.process_time()
        print(f"solution{i} = ", f(grid, pos, direction), time_report(start_time))



GUARD_DIRS = {
    "^": (0, -1),
    ">": (1, 0),
    "<": (-1, 0),
    "v": (0, 1),
}


def solution1(grid: Grid, pos, direction):
    print(pos, direction)
    del grid.grid[pos]
    visited = {pos}
    while True:
        new_pos = pos + direction
        if new_pos in grid.grid:
            direction = rotate(direction)
            continue
        pos = new_pos
        if not grid.in_bounds(pos):
            break
        visited.add(pos)
        # print(f"{steps}:", pos, direction)
        # print(grid.render(overlay={pos:"@"}))
    return len(visited)


def solution2(grid, pos, direction):
    count = 0
    for x in range(grid.x_bounds.max + 1):
        for y in range(grid.y_bounds.max + 1):
            if (x, y) in grid.grid:
                continue
            if contains_loop(grid, pos, direction, Pos(x, y)):
                count += 1
    return count


def contains_loop(grid, pos, direction, obstruction):
    visited = {(pos, direction)}
    while True:
        new_pos = pos + direction
        if new_pos in grid.grid or new_pos == obstruction:
            direction = rotate(direction)
            continue
        pos = new_pos
        if not grid.in_bounds(pos):
            break
        if (pos, direction) in visited:
            return True
        visited.add((pos, direction))
        # print(f"{steps}:", pos, direction)
        # print(grid.render(overlay={pos:"@"}))
    return False


ROTATIONS = {
    (1, 0): (0, 1),
    (-1, 0): (0, -1),
    (0, 1): (-1, 0),
    (0, -1): (1, 0),
}


def rotate(direction):
    return Pos(*ROTATIONS[direction])


def guard_pos(grid):
    for pos, ch in grid.grid.items():
        if ch in GUARD_DIRS:
            return Pos(*pos), Pos(*GUARD_DIRS[ch])
    raise ValueError("No guard found")


if __name__ == "__main__":
    run()

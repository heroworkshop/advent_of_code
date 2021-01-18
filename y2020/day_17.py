from collections import defaultdict

from aocd_tools import load_input_data, grid4d_from_lines


EXAMPLE = """
.#.
..#
###""".strip()


def run():
    input_data = load_input_data(2020, 17)
    print(f"loaded input data ({len(input_data)} bytes)")
    grid = grid4d_from_lines(input_data, default_val=".")
    print("solution1 = ", solution1(grid))
    grid = grid4d_from_lines(input_data, default_val=".")
    print("solution2 = ", solution2(grid))


def count_neighbours(grid, p):
    x, y, z, w = p
    count = 0
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                if dy or dx or dz:
                    np = (x + dx, y + dy, z + dz, w)
                    if np in grid:
                        count += 1
    return count


def count_neighbours4d(grid, p):
    x, y, z, w = p
    count = 0
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                for dw in (-1, 0, 1):
                    if dy or dx or dz or dw:
                        np = (x + dx, y + dy, z + dz, w + dw)
                        if np in grid:
                            count += 1
    return count


def update(grid):
    to_delete = []
    to_add = []
    for p, ch in grid.grid.items():
        x, y, z, w = p
        n = count_neighbours(grid.grid, p)
        if n < 2 or n > 3:
            to_delete.append(p)

    for x in range(grid.x_bounds.min - 1, grid.x_bounds.max + 2):
        for y in range(grid.y_bounds.min - 1, grid.y_bounds.max + 2):
            for z in range(grid.z_bounds.min - 1, grid.z_bounds.max + 2):
                n = count_neighbours(grid.grid, (x, y, z, w))
                if n == 3:
                    to_add.append((x, y, z, w))

    for p in to_delete:
        del grid.grid[p]

    for p in to_add:
        grid.grid[p] = "#"

    grid.update_bounds()


def solution1(grid):
    for i in range(6):
        print(i, ": ", len(grid.grid))
        update(grid)

    return len(grid.grid)


def update4d(grid):
    to_delete = []
    to_add = []
    for p, ch in grid.grid.items():
        x, y, z, w = p
        n = count_neighbours4d(grid.grid, p)
        if n < 2 or n > 3:
            to_delete.append(p)

    for x in range(grid.x_bounds.min - 1, grid.x_bounds.max + 2):
        for y in range(grid.y_bounds.min - 1, grid.y_bounds.max + 2):
            for z in range(grid.z_bounds.min - 1, grid.z_bounds.max + 2):
                for w in range(grid.w_bounds.min - 1, grid.w_bounds.max + 2):
                    n = count_neighbours4d(grid.grid, (x, y, z, w))
                    if n == 3:
                        to_add.append((x, y, z, w))

    for p in to_delete:
        del grid.grid[p]

    for p in to_add:
        grid.grid[p] = "#"

    grid.update_bounds()


def solution2(grid):
    for i in range(6):
        print(i, ": ", len(grid.grid))
        update4d(grid)

    return len(grid.grid)


if __name__ == "__main__":
    run()

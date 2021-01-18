from collections import defaultdict

from aocd_tools import load_input_data, grid_from_lines

EXAMPLE = """
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL""".strip()


def run():
    input_data = load_input_data(2020, 11)
    # input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    grid = grid_from_lines(input_data)

    print("solution1 = ", solution1(grid))
    grid = grid_from_lines(input_data)
    print("solution2 = ", solution2(grid))


def make_grid(lines):
    grid = defaultdict(lambda x: ".")

    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            grid[(x, y)] = ch
    return grid


def count_neighbours(grid, p, ch):
    x, y = p
    count = 0
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dy or dx:
                np = (x + dx, y + dy)
                if np in grid and grid[np] == ch:
                    count += 1
    return count

def count_visible_neighbours(grid, p, ch):
    x, y = p
    count = 0

    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx or dy:
                vx, vy = x, y
                while (vx, vy) in grid:
                    vx += dx
                    vy += dy
                    np = (vx, vy)
                    if np not in grid:
                        break
                    if grid[np] == ch:
                        count += 1
                    if grid[np] != ".":
                        break
    return count


def update(grid):
    new_grid = defaultdict(lambda: ' ')
    for p, ch in grid.items():
        x, y = p
        new_ch = grid[(x, y)]
        if new_ch == "L":
            n = count_neighbours(grid, p, "#")
            if n == 0:
                new_ch = "#"
        elif new_ch == "#":
            n = count_neighbours(grid, p, "#")
            if n >= 4:
                new_ch = "L"
        new_grid[(x, y)] = new_ch
    return new_grid


def new_update(grid):
    new_grid = defaultdict(lambda: ' ')
    for p, ch in grid.items():
        x, y = p
        new_ch = grid[(x, y)]
        if new_ch == "L":
            n = count_visible_neighbours(grid, p, "#")
            if n == 0:
                new_ch = "#"
        elif new_ch == "#":
            n = count_visible_neighbours(grid, p, "#")
            if n >= 5:
                new_ch = "L"
        new_grid[(x, y)] = new_ch
    return new_grid

def solution1(grid):
    old_count = 0
    while True:
        grid.grid = update(grid.grid)
        count = len([c for c in grid.grid.values() if c == "#"])
        if count == old_count:
            break
        old_count = count
    return count


def solution2(grid):
    old_count = 0
    while True:
        print(grid.render())
        grid.grid = new_update(grid.grid)
        count = len([c for c in grid.grid.values() if c == "#"])
        if count == old_count:
            break
        old_count = count
    return count


if __name__ == "__main__":
    run()

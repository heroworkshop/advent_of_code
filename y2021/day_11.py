from collections import deque

from aocd_tools import load_input_data, grid_from_lines

EXAMPLE1 = """11111
19991
19191
19991
11111"""

EXAMPLE = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""


def parse(line):
    return int(line)


def run():
    input_data = load_input_data()
    #input_data  = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    lines = grid_from_lines(input_data, transform=int)
    print("solution1 = ", solution1(lines))
    lines = grid_from_lines(input_data, transform=int)
    print("solution2 = ", solution2(lines))


def on_add(n, p, grid):
    if n == (4, 2):
        print(f"{n} added by {p}")


def solution1(grid):
    flash_count = 0
    for i in range(100):
        print(f"Generation {i}")
        print(grid.render(),"\n")
        flashed = set()
        queue = deque(grid.grid.keys())
        while queue:
            p = queue.popleft()
            if p in flashed:
                continue
            grid.grid[p] += 1
            if grid.grid[p] > 9:
                grid.grid[p] = 0
                flashed.add(p)
                for n in grid.all_existant_neighbours(p):
                    if n not in flashed:
                        queue.append(n)

        flash_count += len(flashed)

    return flash_count


def solution2(grid):
    gen = 0
    while True:
        gen += 1
        print(f"Generation {gen}")
        print(grid.render(), "\n")
        flashed = set()
        queue = deque(grid.grid.keys())
        while queue:
            p = queue.popleft()
            if p in flashed:
                continue
            grid.grid[p] += 1
            if grid.grid[p] > 9:
                grid.grid[p] = 0
                flashed.add(p)
                for n in grid.all_existant_neighbours(p):
                    if n not in flashed:
                        queue.append(n)
        if len(flashed) == len(grid.grid):
            print(f"After Generation {gen}")
            print(grid.render(), "\n")
            return gen


if __name__ == "__main__":
    run()

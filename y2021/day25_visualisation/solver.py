from collections import defaultdict, namedtuple

from grid.model import Grid
from aocd_tools import load_input_data, grid_from_lines

stop_threads = False


def extract_positions(grid, ch):
    return {(x, y)
            for x in range(grid.width)
            for y in range(grid.height)
            if grid.value(x, y) == ch}


def setup_grid():
    input_data = load_input_data(year=2021, day=25)
    print(f"loaded input data ({len(input_data)} bytes)")
    aocd_grid = grid_from_lines(input_data, transform=str)
    grid = Grid(aocd_grid.width, aocd_grid.height)
    grid._values = aocd_grid.grid
    return grid


def run(grid):
    east_movers = extract_positions(grid, ">")
    south_movers = extract_positions(grid, "v")
    print("solution1 = ", solution1(grid, east_movers, south_movers))


def solution1(grid, east_movers, south_movers):
    width, height = grid.width, grid.height
    step = 0
    while not stop_threads:
        count = 0
        step += 1
        movers = dict()
        for p in east_movers:
            x, y = p
            x = (x + 1) % width
            if (x, y) not in east_movers and (x, y) not in south_movers:
                movers[p] = (x, y)
        for p1, p2 in movers.items():
            east_movers.remove(p1)
            grid.fill_cell(*p1, ".")
            east_movers.add(p2)
            grid.fill_cell(*p2, ">")
            count += 1

        movers = dict()
        for p in south_movers:
            x, y = p
            y = (y + 1) % height
            if (x, y) not in east_movers and (x, y) not in south_movers:
                movers[p] = (x, y)
        for p1, p2 in movers.items():
            south_movers.remove(p1)
            grid.fill_cell(*p1, ".")
            south_movers.add(p2)
            grid.fill_cell(*p2, "v")
            count += 1
        if count == 0:
            break

    return step


if __name__ == "__main__":
    run(setup_grid())

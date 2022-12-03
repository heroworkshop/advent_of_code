from aocd_tools import load_input_data, grid_from_lines, Grid

EXAMPLE = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""


def parse(line):
    return [int(c) for c in line]


def run():
    input_data = load_input_data()
    # input_data  = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    # lines = [parse(line) for line in input_data.split("\n")]
    lines = grid_from_lines(input_data, transform=int)
    print("solution1 = ", solution1(lines))
    print("solution2 = ", solution2(lines))


def solution1(grid):
    s = grid.dijkstra((0, 0))
    return s.grid[grid.width - 1, grid.height - 1]


def cap_val(v):
    while v > 9:
        v -= 9
    return v


def solution2(small_grid):
    grid = Grid()
    w = small_grid.width
    h = small_grid.height
    for p in small_grid.grid:
        x, y = p
        for dx in range(5):
            for dy in range(5):
                v = cap_val(small_grid.at(p) + dx + dy)
                dp = dx * w + x, dy * h + y
                grid.add(dp, v)

    print(grid.render())
    s = grid.dijkstra((0, 0))
    return s.grid[grid.width - 1, grid.height - 1]


if __name__ == "__main__":
    run()

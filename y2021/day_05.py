from aocd_tools import load_input_data, Grid


TEST_VALS = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""

def run():
    input_data = load_input_data(2021, 5)
    print(f"loaded input data ({len(input_data)} bytes)")
    # input_data = TEST_VALS
    points = parse_cmds(input_data)

    print("solution1 = ", solution1(points))
    print("solution2 = ", solution2(points))


def parse_coord(coord):
    return [int(p) for p in coord.split(",")]


def parse_cmds(input_data):
    def parse(x):
        return [parse_coord(coords) for coords in x.split(" -> ")]

    lines = input_data.split("\n")
    return [parse(line) for line in lines]


def draw_line(grid: Grid, a, b):
    x0, y0 = a
    x1, y1 = b

    dx = (x1 - x0) // (abs(x1 - x0) or 1)
    dy = (y1 - y0) // (abs(y1 - y0) or 1)
    x, y = x0, y0

    grid.grid[(x, y)] += 1
    while x != x1 or y != y1:
        x += dx
        y += dy
        grid.grid[(x, y)] += 1



def solution1(lines):
    grid = Grid(default_val=0)
    for a, b in lines:
        if a[0] == b[0] or a[1] == b[1]:
            draw_line(grid, a, b)

    return len([v for v in grid.grid.values() if v > 1])


def solution2(lines):
    grid = Grid(default_val=0)
    for a, b in lines:
        draw_line(grid, a, b)

    print(grid.render().replace("0", "."))
    return len([v for v in grid.grid.values() if v > 1])


if __name__ == "__main__":
    run()

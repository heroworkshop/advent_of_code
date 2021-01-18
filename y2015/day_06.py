from collections import defaultdict

from aocd_tools import load_input_data, ints_from_lines, grid_from_lines


EXAMPLE = """
turn on 0,0 through 1,1
toggle 1,1 through 2,2
turn on 2,0 through 2,0
""".strip()

def run():
    input_data = load_input_data(2015, 6)
    # input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    print("solution1 = ", solution1(input_data.split("\n")))
    print("solution2 = ", solution2(input_data.split("\n")))


def parse_coord(c):
    x, _, y = c.partition(",")
    return int(x), int(y)


def parse(line):
    # turn off 660,55 through 986,197
    parts = line.strip().split(" ")
    if line.startswith("turn off"):
        p1 = parse_coord(parts[2])
        p2 = parse_coord(parts[4])
        command = off
    elif line.startswith("turn on"):
        p1 = parse_coord(parts[2])
        p2 = parse_coord(parts[4])
        command = on
    else:
        p1 = parse_coord(parts[1])
        p2 = parse_coord(parts[3])
        command = toggle
    return (p1, p2), command


def toggle(p, grid):
    grid[p] = not grid[p]


def on(p, grid):
    grid[p] = True


def off(p, grid):
    grid[p] = False


def run_cmd(rect, grid, cmd):
    x1, y1 = rect[0]
    x2, y2 = rect[1]
    print(f"{cmd.__name__} ({x1}, {y1}) to ({x2}, {y2})")
    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            cmd((x, y), grid)

    # render(grid)


def render(grid):
    for y in range(3):
        for x in range(3):
            print("*" if grid[(x, y)] else ".", end="")
        print()


def solution1(lines):
    grid = defaultdict(bool)

    for line in lines:
        rect, cmd = parse(line)
        run_cmd(rect, grid, cmd)
    return len([p for p in grid if grid[p]])


def solution2(lines):
    return


if __name__ == "__main__":
    run()

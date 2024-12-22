import re
from aocd_tools import *

EXAMPLE = """#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^"""


def run():
    input_data = load_input_data()
    # input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    # entries = int_tuples_from_lines(lines=input_data, sep=" ")
    a, b = input_data.split("\n\n")
    grid = grid_from_lines(a, default_val=".")
    moves = "".join(b.split("\n"))

    # print(grid.render())

    for i, f in enumerate((solution1, solution2), 1):
        start_time = time.process_time()
        print(f"solution{i} = ", f(grid, moves), time_report(start_time))


def process_one_line(line):
    return line


def solution1(grid, moves):
    return 0
    p, boulders, walls = interpret_grid(grid)
    print(p)
    for move in moves:
        dp = update(move)
        new_p = p + dp
        if new_p in walls:
            continue
        if new_p in boulders:
            dp = push_boulder(new_p, dp, boulders, walls)
            new_p = p + dp

        p = new_p
        # print(render(p, boulders, walls, grid))
    return gps_val(boulders)


def gps_val(boulders):
    total = 0
    for b in boulders:
        total += b[0] + 100 * b[1]
    return total


def push_boulder(p, dp, boulders, walls):
    new_p = p + dp
    if new_p in walls:
        return Pos(0, 0)
    if new_p in boulders:
        dp = push_boulder(new_p, dp, boulders, walls)
    if dp != (0, 0):
        boulders.remove(p)
        boulders.add(new_p)
    return dp


def push_wide_boulder(p, dp, boulders_lhs, boulders_rhs, walls):
    if dp[0]:
        return hpush(p, dp, boulders_lhs, boulders_rhs, walls)
    elif dp[1]:
        return vpush(p, dp, boulders_lhs, boulders_rhs, walls)
    raise RuntimeError


def hpush(p, dp, boulders_lhs, boulders_rhs, walls):
    new_p = p + dp
    if new_p in walls:
        return Pos(0, 0)
    if new_p in boulders_lhs or new_p in boulders_rhs:
        dp = hpush(new_p, dp, boulders_lhs, boulders_rhs, walls)
    if dp != (0, 0):
        if p in boulders_lhs:
            boulders_lhs.remove(p)
            boulders_lhs.add(new_p)
        else:
            boulders_rhs.remove(p)
            boulders_rhs.add(new_p)
    return dp


def vpush(p, dp, boulders_lhs, boulders_rhs, walls) -> Pos:
    to_move = set()
    queue = [p]

    def add_to_queue(pos):
        if pos not in to_move:
            queue.append(pos)

    while queue:
        p = queue.pop(-1)
        if p + dp in walls:
            return Pos(0, 0)
        if p in boulders_lhs:
            add_to_queue(p + Pos(1, 0))
        elif p in boulders_rhs:
            add_to_queue(p + Pos(-1, 0))
        if p + dp in boulders_rhs or p+dp in boulders_lhs:
            add_to_queue(p + dp)
        to_move.add(p)

    add_lhs = set()
    add_rhs = set()
    for p in to_move:
        if p in boulders_lhs:
            boulders_lhs.remove(p)
            add_lhs.add(p + dp)
        elif p in boulders_rhs:
            boulders_rhs.remove(p)
            add_rhs.add(p + dp)

    for p in add_lhs:
        boulders_lhs.add(p)
    for p in add_rhs:
        boulders_rhs.add(p)

    return dp


def solution2(grid, moves):
    p, boulders_lhs, boulders_rhs, walls = interpret_wide_grid(grid)
    print(p)
    for move in moves:
        print(move)
        dp = update(move)
        new_p = p + dp
        if new_p in walls:
            continue
        if new_p in boulders_lhs or new_p in boulders_rhs:
            dp = push_wide_boulder(new_p, dp, boulders_lhs, boulders_rhs, walls)
            new_p = p + dp

        p = new_p
        # print(render_wide(p, boulders_lhs, boulders_rhs, walls, grid))
    return gps_val(boulders_lhs)


def update(move):
    dirs = {"<": (-1, 0),
            ">": (1, 0),
            "^": (0, -1),
            "v": (0, 1)}
    return Pos(*dirs[move])


def interpret_wide_grid(grid):
    p = None
    boulders_lhs = set()
    boulders_rhs = set()
    walls = set()
    for q, v in grid.grid.items():
        x, y = q
        if v == "@":
            p = Pos(x * 2, y)
        elif v == "#":
            walls.add((x * 2, y))
            walls.add((x * 2 + 1, y))
        elif v == "O":
            boulders_lhs.add((x * 2, y))
            boulders_rhs.add((x * 2 + 1, y))
    return p, boulders_lhs, boulders_rhs, walls


def interpret_grid(grid):
    p = None
    boulders = set()

    walls = set()
    for q, v in grid.grid.items():
        if v == "@":
            p = Pos(*q)
        elif v == "#":
            walls.add(q)
        elif v == "O":
            boulders.add(q)
    return p, boulders, walls


def extract_lines(entries):
    return entries.split("\n")


def render(pos, boulders, walls, grid):
    lines = []
    for y in range(grid.height):
        line = ""
        for x in range(grid.width):
            p = Pos(x, y)
            if p in walls:
                line += "#"
            elif p in boulders:
                line += "O"
            elif p == pos:
                line += "@"
            else:
                line += "."
        lines.append(line)
    return "\n".join(lines)


def render_wide(pos, boulders_lhs, boulders_rhs, walls, grid):
    lines = []
    for y in range(grid.height):
        line = ""
        for x in range(grid.width * 2):
            p = Pos(x, y)
            if p in walls:
                line += "#"
            elif p in boulders_lhs:
                line += "["
            elif p in boulders_rhs:
                line += "]"
            elif p == pos:
                line += "@"
            else:
                line += "."
        lines.append(line)
    return "\n".join(lines)


if __name__ == "__main__":
    run()

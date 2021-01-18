from collections import defaultdict

from aocd_tools import load_input_data, ints_from_lines, grid_from_lines


def run():
    input_data = load_input_data(2015, 3)
    print(f"loaded input data ({len(input_data)} bytes)")
    print("solution1 = ", solution1(input_data))
    print("solution2 = ", solution2(input_data))


INSTRUCTIONS = {
    ">":(1, 0),
    "<": (-1, 0),
    "v": (0, 1),
    "^": (0, -1)
}


def solution1(moves):
    grid = defaultdict(int)
    x, y = 0, 0

    for move in moves:
        v = INSTRUCTIONS[move]
        x += v[0]
        y += v[1]
        grid[(x, y)] += 1
    return len(grid)


def solution2(moves):
    grid = defaultdict(int)
    x = [0, 0]
    y = [0, 0]

    n = 0

    for move in moves:
        v = INSTRUCTIONS[move]
        i = n % 2
        x[i] += v[0]
        y[i] += v[1]
        grid[(x[i], y[i])] += 1
        n += 1
    return len(grid)


if __name__ == "__main__":
    run()

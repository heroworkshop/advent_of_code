from collections import defaultdict, namedtuple


from aocd_tools import load_input_data


EXAMPLE = """target area: x=20..30, y=-10..-5\n"""


def parse(line):
    _, _, lo_hi = line[:-1].partition("=")
    lo, hi = [int(v) for v in lo_hi.split("..")]
    return lo, hi


def run():
    input_data = load_input_data() + "\n"
    # input_data  = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    parts = input_data.split(" ")[2:]
    x_range, y_range = [parse(line) for line in parts]
    # lines = grid_from_lines(input_data, transform=int)
    print("solution1 = ", solution1(x_range, y_range))
    print("solution2 = ", solution2(x_range, y_range))


def is_in_target_range(x, y, x_range, y_range):
    return min(x_range) <= x <= max(x_range) and min(y_range) <= y <= max(y_range)


def solution1(x_range, y_range):
    print(f"x_range: {x_range}")
    print(f"y_range: {y_range}")

    results = defaultdict(list)
    best_height = 0
    winning_moves = set()
    steps = 1000 - y_range[0] + 1
    ds = steps//100
    for y_vel0 in range(y_range[0] - 1, 1000):
        # if y_vel0 % ds == 0:
        #    print("#", end="")
        print()
        for x_vel0 in range(1, x_range[1] + 1):
            x, y = 0, 0
            x_vel, y_vel = x_vel0, y_vel0
            max_height = 0
            # print(f"({x_vel}, {y_vel}):", end="")
            while x < x_range[1] and y > y_range[0]:
                x += x_vel
                y += y_vel
                # print(f" ({x}, {y})", end="")
                # results[(x_vel0, y_vel0)].append((x, y))
                x_vel = max(0, x_vel - 1)
                y_vel -= 1
                max_height = max(max_height, y)
                if is_in_target_range(x, y, x_range, y_range):
                    best_height = max(best_height, max_height)
                    winning_moves.add((x_vel0, y_vel0))
                    print((x_vel0, y_vel0), f"[{x}, {y}]", end=" ")
                    break

    print()
    # check(winning_moves, results)
    return best_height, len(winning_moves)


def check(moves, results):
    def make_coord(ab):
        return tuple([int(v) for v in ab.split(",")])

    expected = """23,-10  25,-9   27,-5   29,-6   22,-6   21,-7   9,0     27,-7   24,-5
25,-7   26,-6   25,-5   6,8     11,-2   20,-5   29,-10  6,3     28,-7
8,0     30,-6   29,-8   20,-10  6,7     6,4     6,1     14,-4   21,-6
26,-10  7,-1    7,7     8,-1    21,-9   6,2     20,-7   30,-10  14,-3
20,-8   13,-2   7,3     28,-8   29,-9   15,-3   22,-5   26,-8   25,-8
25,-6   15,-4   9,-2    15,-2   12,-2   28,-9   12,-3   24,-6   23,-7
25,-10  7,8     11,-3   26,-7   7,1     23,-9   6,0     22,-10  27,-6
8,1     22,-8   13,-4   7,6     28,-6   11,-4   12,-4   26,-9   7,4
24,-10  23,-8   30,-8   7,0     9,-1    10,-1   26,-5   22,-9   6,5
7,5     23,-6   28,-10  10,-2   11,-1   20,-9   14,-2   29,-7   13,-3
23,-5   24,-8   27,-9   30,-7   28,-5   21,-10  7,9     6,6     21,-5
27,-10  7,2     30,-9   21,-8   22,-7   24,-9   20,-6   6,9     29,-5
8,-2    27,-8   30,-5   24,-7"""
    expected = set([make_coord(x) for x in expected.split()])

    print("missing:", expected.difference(moves))
    for c in expected.difference(moves):
        print(f"{c}: {results[c]}")
    print("extra:", moves.difference(expected))


def solution2(x_range, y_range):
    return None


if __name__ == "__main__":
    run()

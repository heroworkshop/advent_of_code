from aocd_tools import load_input_data


def parse(line):
    return int(line)


def run():
    input_data = load_input_data()
    # input_data = "16,1,2,0,4,2,7,1,2,14"
    print(f"loaded input data ({len(input_data)} bytes)")
    lines = [parse(line) for line in input_data.split(",")]
    print("solution1 = ", solution1(lines))
    print("solution2 = ", solution2(lines))


def solution1(positions):
    costs = {move_to: sum([abs(move_to - p) for p in positions])
             for move_to in range(min(positions), max(positions) + 1)
             }

    return min(costs.values())


def calc_cost(d):
    return (1 + d) * d // 2


def solution2(positions):
    costs = {move_to: sum([calc_cost(abs(move_to - p)) for p in positions])
             for move_to in range(min(positions), max(positions) + 1)
             }

    return min(costs.values())


if __name__ == "__main__":
    run()

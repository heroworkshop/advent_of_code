from collections import defaultdict
from contextlib import suppress

from aocd_tools import load_input_data


def parse(line):
    return int(line)


def run():
    input_data = load_input_data(2020, 15)
    print(f"loaded input data ({len(input_data)} bytes)")
    lines = [parse(line) for line in input_data.split(",")]
    print("solution1 = ", solution1(lines))
    lines = [parse(line) for line in input_data.split(",")]
    print("solution2 = ", solution2(lines))


def solution1(lines):
    history = defaultdict(list)
    for turn in range(1, 2021):
        if lines:
            spoken = lines.pop(0)
        else:
            previous = history[spoken]
            if len(previous) == 1:
                spoken = 0
            else:
                spoken = previous[-1] - previous[-2]
        history[spoken].append(turn)
        print(turn, spoken)

    return spoken


def solution2(lines):
    history = defaultdict(list)
    for turn in range(1, 30000001):
        if lines:
            spoken = lines.pop(0)
        else:
            previous = history[spoken]
            if len(previous) == 1:
                spoken = 0
            else:
                spoken = previous[-1] - previous[-2]
        history[spoken].append(turn)
        if turn % 1000000 == 0:
            print(turn, spoken)

    return spoken


if __name__ == "__main__":
    run()

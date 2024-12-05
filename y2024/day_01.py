from aocd_tools import *


def run():
    input_data = load_input_data(2024, 1)
    print(f"loaded input data ({len(input_data)} bytes)")
    entries = int_tuples_from_lines(lines=input_data, sep=" ")
    # lines = input_data.split("\n")
    # entries = [process_one_line(line) for line in lines]
    print(entries)

    left, right = zip(*entries)

    print("solution1 = ", solution1(left, right))
    print("solution2 = ", solution2(left, right))


def process_one_line(line):
    return tuple(int(p) for p in line.split())


def solution1(left, right):
    left = sorted(left)
    right = sorted(right)
    diffs = [abs(a - b) for a, b in zip(left, right)]
    return sum(diffs)


def solution2(left, right):
    values = [p * right.count(p) for p in left]
    return sum(values)


if __name__ == "__main__":
    run()

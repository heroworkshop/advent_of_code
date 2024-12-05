from aocd_tools import *


def run():
    input_data = load_input_data(2024, 2)
    print(f"loaded input data ({len(input_data)} bytes)")
    entries = int_tuples_from_lines(lines=input_data, sep=" ")

    print(entries)

    for i, f in enumerate((solution1, solution2), 2):
        print(f"solution{i} = ", f(entries))


def process_one_line(line):
    deltas = [b - a for a, b in zip(line[:-1], line[1:])]
    if not all(deltas):
        return 0
    direction = deltas[0] / abs(deltas[0])
    if not all(d / abs(d) == direction for d in deltas):
        return 0

    if not all(abs(d) < 4 for d in deltas):
        return 0

    return 1


def process_one_line_with_dampers(line):
    if process_one_line(line):
        return 1
    for i in range(len(line)):
        adjusted_line = line[:i] + line[i + 1:]
        if process_one_line(adjusted_line):
            return 1
    return 0


def solution1(entries):
    return sum(process_one_line(line) for line in entries)


def solution2(entries):
    return sum(process_one_line_with_dampers(line) for line in entries)


if __name__ == "__main__":
    run()

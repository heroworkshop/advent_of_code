from pathlib import Path

from aocd_tools import load_input_data


def parse(line):
    return int(line)


def run():
    year = int(Path(__file__).parent.stem[1:])
    day = int(Path(__file__).stem[4:6])
    print(f"Advent of Code {year}, day {day}")
    input_data = load_input_data(year, day)
    print(f"loaded input data ({len(input_data)} bytes)")
    lines = [parse(line) for line in input_data.split("\n")]
    print("solution1 = ", solution1(lines))
    print("solution2 = ", solution2(lines))


def solution1(lines):
    return


def solution2(lines):
    return


if __name__ == "__main__":
    run()

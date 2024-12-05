import re
from aocd_tools import *


EXAMPLE = """
"""

def run():
    input_data = load_input_data(2024, 5)
    # input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    # entries = int_tuples_from_lines(lines=input_data, sep=" ")
    entries = input_data



    print(entries)

    for i, f in enumerate((solution1, solution2), 1):
        print(f"solution{i} = ", f(entries))


def process_one_line(line):
    return line


def solution1(entries):
    lines = extract_lines(entries)
    print(lines)
    return sum(process_one_line(line) for line in lines)


def solution2(entries):
    lines = extract_lines(entries)
    print(lines)
    return sum(process_one_line(line) for line in lines)


def extract_lines(entries):
    return entries.split("\n")


if __name__ == "__main__":
    run()

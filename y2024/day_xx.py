import re
from aocd_tools import *


EXAMPLE = """
"""

def run():
    input_data = load_input_data()
    # input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    # entries = int_tuples_from_lines(lines=input_data, sep=" ")
    # a, b = entries.split("\n\n")
    entries = [process_one_line(line) for line in input_data.splitlines()]

    print(entries)

    for i, f in enumerate((solution1, solution2), 1):
        start_time = time.process_time()
        print(f"solution{i} = ", f(entries), time_report(start_time))


def process_one_line(line):
    return line

def solution1(entries):
    return 0

def solution2(entries):
    return 0


def extract_lines(entries):
    return entries.split("\n")


if __name__ == "__main__":
    run()

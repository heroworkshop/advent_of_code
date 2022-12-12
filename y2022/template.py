from collections import deque
from dataclasses import dataclass
from typing import NamedTuple, List

from aocd_tools import load_input_data

EXAMPLE = """
"""


def run():
    input_data = load_input_data(2022, 11)
    input_data = EXAMPLE

    print(f"loaded input data ({len(input_data)} bytes)")

    entries = input_data.split("\n\n")
    entries = [parse(line) for line in entries]
    print(entries[:50])

    print("solution1 = ", solution1(entries))

    print("solution2 = ", solution2(entries))


def parse(line: str):
    return [int(item) for item in line.split()]
    # return [ord(ch) for ch in line]
    # return line


def solution1(entries):
    return


def solution2(entries):
    return


if __name__ == "__main__":
    run()

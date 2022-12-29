from collections import deque
from dataclasses import dataclass
from typing import NamedTuple, List

from aocd_tools import load_input_data

EXAMPLE = """
"""


def run():
    input_data = load_input_data(2022, 25)
    # input_data = EXAMPLE

    print(f"loaded input data ({len(input_data)} bytes)")

    entries = input_data.split("\n")
    entries = [from_snafu(line) for line in entries]
    print(entries[:50])

    print("solution1 = ", solution1(entries))

    print("solution2 = ", solution2(entries))


SNAFU_VALS = ["=", "-", "0", "1", "2"]


def from_snafu(line: str) -> int:
    total = 0
    for index, part in enumerate(reversed(line)):
        v = SNAFU_VALS.index(part) - 2
        total += 5 ** index * v
    return total


def to_snafu(decint: int) -> str:
    result = ""
    while decint:
        remainder = decint % 5
        decint //= 5
        result = "012=-"[remainder] + result
        if remainder in (3, 4):
            # base-5 4 == snafu 1-
            # base-5 3 == snafu 1=
            decint += 1

    return result


def solution1(entries):
    total = sum(entries)
    print(total)
    return to_snafu(total)


def solution2(entries):
    return


if __name__ == "__main__":
    run()

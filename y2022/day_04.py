from typing import NamedTuple

from aocd_tools import load_input_data

EXAMPLE = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""


class assignment:
    def __init__(self, s):
        vals = s.split("-")
        self.lower, self.upper = [int(i) for i in vals]

    def __repr__(self):
        return f"{self.lower} to {self.upper}"


def run():
    input_data = load_input_data(2022, 4)
    # input_data = EXAMPLE

    print(f"loaded input data ({len(input_data)} bytes)")

    entries = input_data.split("\n")
    entries = [parse_item(e) for e in entries]
    print(entries[:50])

    print("solution1 = ", solution1(entries))
    print("solution2 = ", solution2(entries))


def parse_item(item_str):
    pairs = item_str.split(",")
    pair = [assignment(a) for a in pairs]
    return pair


def solution1(entries):
    total = 0
    for e in entries:
        left, right = e
        if left.lower <= right.lower and left.upper >= right.upper:
            total += 1
        elif right.lower <= left.lower and right.upper >= left.upper:
            total += 1
    return total


def solution2(entries):
    total = 0
    for e in entries:
        left, right = e
        lr = set(range(left.lower, left.upper + 1))
        rr = set(range(right.lower, right.upper + 1))
        if lr.intersection(rr):
            total += 1

    return total


if __name__ == "__main__":
    run()

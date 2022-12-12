from typing import NamedTuple

from aocd_tools import load_input_data

EXAMPLE = """10000"""


class assignment:
    def __init__(self, s):
        vals = s.split("-")
        self.lower, self.upper = [int(i) for i in vals]

    def __repr__(self):
        return f"{self.lower} to {self.upper}"


def run():
    input_data = load_input_data(2016, 16)
    # input_data = EXAMPLE

    print(f"loaded input data ({len(input_data)} bytes)")


    print(input_data[:50])

    print("solution1 = ", solution1(input_data))
    print("solution2 = ", solution2(input_data))

def flip(ch):
    return "0" if ch == "1" else "1"


def extend(a):
    b = [flip(x) for x in a[::-1]]

    return a + "0" + "".join(b)


def solution1(s):
    target = 272
    while len(s) < target:
        s = extend(s)
    s = s[:target]
    s = checksum(s)
    return s


def encode(a, b):
    return "1" if a == b else "0"

def checksum(s):
    while True:
        s = [encode(a, b) for a, b in zip(s[::2], s[1::2])]
        if len(s) % 2:
            return "".join(s)

def solution2(s):
    target = 35651584

    while len(s) < target:
        s = extend(s)
    s = s[:target]
    print(s)
    s = checksum(s)
    return s


if __name__ == "__main__":
    run()

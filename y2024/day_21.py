import re
from aocd_tools import *

EXAMPLE = """029A
980A
179A
456A
379A"""

INPUT_DATA = """319A
985A
340A
489A
964A"""

def run():
    input_data = INPUT_DATA
    input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")

    entries = input_data.splitlines()

    for i, f in enumerate((solution1, solution2), 1):
        start_time = time.process_time()
        print(f"solution{i} = ", f(entries), time_report(start_time))


def get_key_presses(s):
    keys1 = directions_from_numeric(s)
    keys2 = indirect_keys_from_directions(keys1)
    keys3 = indirect_keys_from_directions(keys2)
    return keys3


NUMERIC_PAD = {
    "7": (0, 0),
    "8": (1, 0),
    "9": (2, 0),
    "4": (0, 1),
    "5": (1, 1),
    "6": (2, 1),
    "1": (0, 2),
    "2": (1, 2),
    "3": (2, 2),
    "0": (1, 3),
    "A": (2, 3),
}


DIRECTION_PAD = {
    "^": (1, 0),
    "A": (2, 0),
    "<": (0, 1),
    "v": (1, 1),
    ">": (2, 1),
}

def press_numeric(current, target):
    p0 = Pos(*NUMERIC_PAD[current])
    p1 = Pos(*NUMERIC_PAD[target])

    d = p1 - p0
    moves = ""
    if d.x > 0:
        moves += ">" * d.x
    if d.y < 0:
        moves += "^" * abs(d.y)
    if d.x < 0:
        moves += "<" * abs(d.x)
    if d.y > 0:
        moves += "v" * d.y
    return moves


def press_direction(current, target):
    p0 = Pos(*DIRECTION_PAD[current])
    p1 = Pos(*DIRECTION_PAD[target])

    d = p1 - p0
    moves = ""
    if d.x > 0:
        moves += ">" * d.x
    if d.y > 0:
        moves += "v" * d.y
    if d.y < 0:
        moves += "^" * abs(d.y)
    if d.x < 0:
        moves += "<" * abs(d.x)
    return moves


def directions_from_numeric(keys):
    p = "A"
    result = ""
    for key in keys:
        result += press_numeric(p, key) + "A"
        p = key
    return result


def indirect_keys_from_directions(keys):
    p = "A"
    result = ""
    for key in keys:
        result += press_direction(p, key) + "A"
        p = key
    return result



def solution1(entries):
    result = 0
    for line in entries:
        keys = get_key_presses(line)
        a = len(keys)
        b = int(line[:-1])
        m = a * b
        print(f"{line} {keys} {m} = {a}  {b}")
        result += m
    return result


def solution2(entries):
    return 0


def extract_lines(entries):
    return entries.split("\n")


if __name__ == "__main__":
    run()

import re
from collections import defaultdict
from functools import cache

from aocd_tools import *

EXAMPLE = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""


def run():
    input_data = load_input_data()  # noqa: F405
    # input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    a, b = input_data.split("\n\n")
    patterns = a.split(", ")
    designs = b.split("\n")

    print(patterns)

    for i, f in enumerate((solution1, solution2), 1):
        start_time = time.process_time()
        print(f"solution{i} = ", f(patterns, designs), time_report(start_time))


def process_one_line(line):
    return line


known_possibles = set()


pattern_dict: dict[str, list[str]]

@cache
def is_possible(design: str):
    try:
        patterns = pattern_dict[design[0]]
    except KeyError:
        return False
    for p in patterns:
        if design.startswith(p):
            new_d = design[len(p):]
            if not new_d:
                return True
            if is_possible(new_d):
                return True
    return False


@cache
def count_possible(design: str):
    try:
        patterns = pattern_dict[design[0]]
    except KeyError:
        return 0
    count = 0
    for p in patterns:
        if design.startswith(p):
            new_d = design[len(p):]
            if not new_d:
                count += 1
                continue
            count += count_possible(new_d)
    return count

def make_pattern_dict(patterns: list[str]) -> dict[str, list[str]]:
    result = defaultdict(list)
    for pattern in patterns:
        key = pattern[0]
        result[key].append(pattern)
    return dict(result)


def solution1(patterns: list[str], designs: list[str]):
    global pattern_dict
    pattern_dict = make_pattern_dict(patterns)
    count = 0
    for design in designs:
        if is_possible(design):
            count += 1

    return count



def solution2(patterns, designs):
    count = 0
    for design in designs:
        count += count_possible(design)

    return count


if __name__ == "__main__":
    run()

import itertools
import re
from collections import defaultdict
from pprint import pprint
from typing import Tuple

from aocd_tools import *

EXAMPLE = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""


def run():
    input_data = load_input_data()
    # input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    entries = input_data

    # print(entries)

    for i, f in enumerate((solution1, solution2), 1):
        start_time = time.process_time()
        print(f"solution{i} = ", f(entries), time_report(start_time))


def process_one_line(line: Tuple[int, ...], rules: Tuple[int, int]):
    for a, b in rules:
        try:
            if line.index(a) > line.index(b):
                return 0
        except ValueError:
            pass
    center = len(line) // 2
    return line[center]


def process_one_incorrect_line(line: Tuple[int, ...], rules: set[Tuple[int, int]]):
    breaking_rules = []
    for a, b in rules:
        try:
            if line.index(a) > line.index(b):
                breaking_rules.append((a, b))
        except ValueError:
            pass

    if not breaking_rules:
        return 0

    # print(f"solving {line}:")

    ordered = reorder(line, rules)
    return ordered[len(ordered) // 2]


def reorder(line: Tuple[int, ...], rules: set[Tuple[int, int]]):
    if len(line) <= 0:
        return line
    x = line[0]
    lhs = []
    rhs = []
    for v in line[1:]:
        if (x, v) in rules:
            # x,v not allowed, so must be v, x
            lhs.append(v)
        else:
            # x, v is allowed so add it
            rhs.append(v)
    return reorder(lhs, rules) + [x] + reorder(rhs, rules)


def solution1(entries):
    rules_block, updates_block = entries.split("\n\n")
    rules = extract_rules(rules_block)
    updates = extract_updates(updates_block)
    return sum(process_one_line(line, rules) for line in updates)


def solution2(entries):
    rules_block, updates_block = entries.split("\n\n")
    rules = extract_rules(rules_block)
    updates = extract_updates(updates_block)
    return sum(process_one_incorrect_line(line, rules) for line in updates)


def extract_rules(rules_block):
    return set(int_tuples_from_lines(lines=rules_block, sep="|"))


def extract_updates(block):
    return int_tuples_from_lines(lines=block, sep=",")


def extract_lines(entries):
    return entries.split("\n")


if __name__ == "__main__":
    run()

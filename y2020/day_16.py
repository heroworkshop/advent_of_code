from collections import namedtuple
from typing import List

from aocd_tools import load_input_data

Rule = namedtuple("rule", "name valid_values")


def parse_ticket(line):
    return [int(v) for v in line.split(",")]


def parse_rules(line):
    name, _, range_spec = line.partition(":")
    parts = range_spec.split()
    valid_values = set()
    for p in parts:
        if "-" in p:
            low, _, high = p.partition("-")
            for v in range(int(low), int(high) + 1):
                valid_values.add(v)
    return Rule(name, valid_values)


def run():
    input_data = load_input_data(2020, 16)
    print(f"loaded input data ({len(input_data)} bytes)")
    sections = input_data.split("\n\n")
    rules = [parse_rules(line) for line in sections[0].strip().split("\n")]

    my_ticket = parse_ticket(sections[1].strip().split("\n")[-1])
    tickets = [parse_ticket(line) for line in sections[2].strip().split("\n")[1:]]
    print("solution1 = ", solution1(rules, tickets))
    print("solution2 = ", solution2(rules, tickets, my_ticket))


def solution1(rules, tickets):
    print(rules)
    print(tickets)
    combined_rules = combine(rules)
    total = 0
    for t in tickets:
        for v in t:
            if v not in combined_rules:
                total += v
    return total


def valid(ticket, rules):
    for v in ticket:
        if v not in rules:
            return False
    return True


def combine(rules: List[Rule]):
    combined_rules = set()
    for r in rules:
        combined_rules = combined_rules.union(r.valid_values)
    return combined_rules


def order_is_correct(ordered_rules, valid_tickets):
    for ticket in valid_tickets:
        for v, rule in zip(ticket, ordered_rules):
            if v not in rule.valid_values:
                return False
    return True


def find_possible(rule, tickets):
    print(f"Analysing rule '{rule.name}'")

    def position_is_possible(index):
        for t_num, t in enumerate(tickets):
            if t[index] not in rule.valid_values:
                print(f"    Position {index} invalidated by ticket {t_num} ({t[index]})")
                return False
        return True

    return set([i for i in range(len(tickets[0])) if position_is_possible(i)])


def solution2(rules, tickets, my_ticket):
    print(f"Out of {len(tickets)} tickets,")
    combined_rules = combine(rules)
    valid_tickets = [t for t in tickets if valid(t, combined_rules)]
    print(f"Found {len(valid_tickets)} valid tickets")

    possible_positions = {r.name: find_possible(r, valid_tickets) for r in rules}

    solved = {}

    while True:
        done = {n: p for n, p in possible_positions.items() if len(p) == 1}
        solved.update(done)
        possible_positions = {n: p for n, p in possible_positions.items() if len(p) > 1}
        to_cull = set()
        for v in done.values():
            to_cull.update(v)
        if not to_cull:
            break
        print(f"culling values {to_cull}")
        for p in possible_positions.values():
            p.difference_update(to_cull)

    print("UNSOLVED")
    for name, possible in possible_positions.items():
        print(name, ": ", possible)

    print("SOLVED:")
    result = 1
    for name, index in solved.items():
        print(name, ": ", index)
        if name.startswith("departure"):
            result *= my_ticket[index.pop()]

    return result


if __name__ == "__main__":
    run()

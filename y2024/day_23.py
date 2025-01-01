import re
from collections import defaultdict

from aocd_tools import *

EXAMPLE = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""


def run():
    input_data = load_input_data()
    # input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    entries = [process_one_line(line) for line in input_data.splitlines()]

    print(entries)

    for i, f in enumerate((solution1, solution2), 1):
        start_time = time.process_time()
        print(f"solution{i} = ", f(entries), time_report(start_time))


def process_one_line(line):
    return tuple(line.split("-"))


def solution1(entries):
    networks = find_networks(entries)
    t_networks = select_t_networks(networks)
    return len(t_networks)


def solution2(entries):
    best = set()
    nodes = get_node_connections(entries)
    networks = list(find_networks(entries))
    for i, network in enumerate(networks):
        trial_solution = set(network)
        for add_n in networks[i:]:
            for name in add_n:

    return 0


def find_networks(entries: list[tuple[str, str]]) -> set[tuple[str, str]]:
    found = set()
    nodes = get_node_connections(entries)

    for name, connections1 in nodes.items():
        for c1_name in connections1:
            connections2 = nodes[c1_name]
            for c2_name in connections2:
                if c2_name == name:
                    continue
                connections3 = nodes[c2_name]
                if name in connections3:
                    match = tuple(sorted([name, c1_name, c2_name]))
                    found.add(match)
                    print(match)

    return found


def get_node_connections(entries):
    nodes = defaultdict(set)
    for a, b in entries:
        nodes[a].add(b)
        nodes[b].add(a)
    return nodes


def select_t_networks(networks: set[tuple[str, str]]) -> set[tuple[str, str]]:
    selected = set()
    for network in networks:
        for name in network:
            if name.startswith("t"):
                selected.add(network)
                break
    return selected


if __name__ == "__main__":
    run()

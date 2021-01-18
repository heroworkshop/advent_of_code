from collections import defaultdict, namedtuple, deque
from typing import List

from aocd_tools import load_input_data

Node = namedtuple("node", "id children")


def parse(line):
    name, _, children = line.partition("<->")
    return Node(int(name), {int(c) for c in children.split(",")})


def run():
    input_data = load_input_data(2017, 12)
    print(f"loaded input data ({len(input_data)} bytes)")
    lines = [parse(line) for line in input_data.split("\n")]
    print("solution1 = ", solution1(lines))
    print("solution2 = ", solution2(lines))


def solution1(nodes: List[Node]):
    network = make_network(nodes)

    found = enumerate_group(network, 0)

    return len(found)


def make_network(nodes):
    network = defaultdict(set)
    for node in nodes:
        for child in node.children:
            network[node.id].add(child)
            network[child].add(node.id)
    return network


def solution2(nodes):
    network = make_network(nodes)

    group_count = 0
    found = set()
    for node_id in network:
        if node_id not in found:
            group = enumerate_group(network, node_id)
            group_count += 1
            for c in group:
                found.add(c)

    return group_count


def enumerate_group(network, connected_to):
    queue = deque([connected_to])
    found = set()
    while queue:
        node_id = queue.popleft()
        found.add(node_id)
        children = network[node_id]
        for child in children:
            if child not in found:
                queue.append(child)
    return found


if __name__ == "__main__":
    run()

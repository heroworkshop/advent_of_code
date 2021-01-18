from collections import defaultdict

from aocd_tools import load_input_data


EXAMPLE = """
pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)""".strip()


class UnbalancedLoad(ValueError):
    def __init__(self, v):
        self.required_weight = v
        super().__init__(f"Encountered unbalanced load. Required weight = {v}")


class Node:
    def __init__(self, name, weight, children):
        self.name = name
        self.weight = weight
        self.children = children
        self.parent = None


def parse(line):
    node_str, _, children = line.partition("->")
    if children:
        children = children.strip().split(", ")
    else:
        children = []
    name, _, weight = node_str.partition(" (")
    weight = int(weight.strip()[:-1])
    name = name.strip()
    print(f"{name} {weight} {children}")
    return Node(name, weight, children)


def run():
    input_data = load_input_data(2017, 7)
    # input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    nodes = [parse(line) for line in input_data.split("\n")]
    tree = make_tree(nodes)
    print("solution1 = ", solution1(tree))
    print("solution2 = ", solution2(tree))


def solution1(tree):
    root = find_root(tree)
    return root.name


def find_root(tree: dict) -> Node:
    node = next(iter(tree.values()))
    while node.parent:
        node = tree[node.parent]
    return node


def make_tree(nodes):
    tree = {node.name: node for node in nodes}
    for node in nodes:
        for child in node.children:
            tree[child].parent = node.name
    return tree


def solution2(tree):
    root = find_root(tree)
    try:
        total_load = calculate_load(root, tree)
    except UnbalancedLoad as e:
        return e.required_weight


def calculate_load(node, tree):
    tally = defaultdict(int)
    weights = {}
    for child in node.children:
        weight = calculate_load(tree[child], tree)
        tally[weight] += 1
        weights[weight] = child

    if len(tally) > 1:
        # One of the weights is different
        wrong = [weight for weight, count in tally.items() if count == 1]
        correct = [weight for weight, count in tally.items() if count > 1]
        diff = correct[0] - wrong[0]
        wrong_child = weights[wrong[0]]
        raise UnbalancedLoad(tree[wrong_child].weight + diff)
    print(f"{node.name} = {node.weight} + {tally}")
    return node.weight + sum([v*count for v, count in tally.items()])


if __name__ == "__main__":
    run()

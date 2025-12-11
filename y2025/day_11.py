from collections import deque
from pprint import pprint

from y2025.day11_data import DATA

EXAMPLE = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
""".strip()

EXAMPLE_2 = """
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out"""

def parse(data):
    lines = [line.strip() for line in data.strip().split("\n")]
    return lines


def part1():
    rows = parse(DATA)
    nodes = {}

    for row in rows:
        node, _, connections = row.partition(":")
        nodes[node] = connections.split()
    print(nodes)
    paths = find_all_possible_paths(nodes, "you", "out")

    return len(paths)

def find_all_possible_paths(nodes, start, finish):
    paths = []
    queue = deque()

    queue.append((start, {start}))
    print(queue)
    while queue:
        node = queue.popleft()
        if node[0] == finish:
            paths.append(node)
            continue
        visited = node[1]
        for p in nodes[node[0]]:
            if p not in visited:
                queue.append((p, {*visited, p}))
    return paths

def part2():
    rows = parse(DATA)
    nodes = {}

    for row in rows:
        node, _, connections = row.partition(":")
        nodes[node] = connections.split()
    print(nodes)
    paths = find_all_possible_paths2(nodes, "svr", "out")
    pprint(paths)

    valid_paths = [path for path in paths if "fft" in path and "dac" in path]
    return len(valid_paths)

def find_all_possible_paths2(nodes, start, finish):
    paths = []
    queue = deque()

    queue.append((start, {start}))
    print(queue)
    while queue:
        node = queue.popleft()
        if node[0] == finish:
            paths.append(node[1])
            print(node[1])
            continue
        visited = node[1]
        for p in nodes[node[0]]:
            if p not in visited:
                queue.append((p, {*visited, p}))
    return paths

if __name__ == "__main__":
    print("part1:", part1())
    print("part2:", part2())

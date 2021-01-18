from collections import namedtuple
from itertools import permutations

from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree

from aocd_tools import load_input_data


EXAMPLE = """
London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141""".strip()

Edge = namedtuple("edge", "a b length")


def run():
    input_data = load_input_data(2015, 9)
    # input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    solution = solution1(input_data.split("\n"))
    print("solution1 = ", solution[0])
    print("solution2 = ", solution[1])


def parse_edge(line):
    parts = line.split(" ")
    return Edge(parts[0], parts[2], int(parts[4]))


def solution1(lines):
    edges = [parse_edge(line) for line in lines]
    print(edges)

    places = list({edge.a for edge in edges}.union({edge.b for edge in edges}))
    print(places)

    indices = {v: i for i, v in enumerate(places)}
    print(indices)

    table = make_distance_table(edges, indices, places)

    distances = []

    for route in permutations(indices.values()):
        prev = None
        total = 0
        for p in route:
            if prev is not None:
                total += table[p][prev] + table[prev][p]
            prev = p
        distances.append(total)

    #mst = minimum_spanning_tree(table)
    #routes = mst.toarray().astype(int)
    #print(routes)
    #lengths = [sum(row) for row in routes]
    return min(distances), max(distances)


def make_distance_table(edges, indices, places):
    table = [[0] * len(places) for i in range(len(places))]
    for edge in edges:
        a_index = indices[edge.a]
        b_index = indices[edge.b]
        table[a_index][b_index] = edge.length
    print(table)
    return table


if __name__ == "__main__":
    run()

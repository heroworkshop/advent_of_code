import itertools

from y2025.day08_data import DATA

EXAMPLE = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
""".strip()

def parse(data):
    lines = [line.strip().split(",") for line in data.strip().split("\n")]
    return lines

def part1():
    str_rows = parse(DATA)
    rows = [tuple(map(int, row)) for row in str_rows]
    distances = sorted([(distance_squared(a, b), a, b) for a, b in itertools.combinations(rows, 2)])
    # pprint(distances)

    network = {
        net: net_id
        for net_id, net in enumerate(rows)
    }

    for (_, a, b) in distances[:1000]:
        # move b and all items in network b to a
        from_net_id = network[b]

        for p in network:  # reassign all matching nodes
            if network[p] == from_net_id:
                network[p] = network[a]

    # size all the networks
    size_by_net_id = {}
    for _, v in network.items():
        size_by_net_id[v] = size_by_net_id.get(v, 0) + 1

    sizes = sorted(size_by_net_id.values(), reverse=True)

    return sizes[0] * sizes[1] * sizes[2]


def distance_squared(a, b):
    return abs(a[0] - b[0]) ** 2 + abs(a[1] - b[1]) ** 2 + abs(a[2] - b[2]) ** 2

def part2():
    str_rows = parse(DATA)
    rows = [tuple(map(int, row)) for row in str_rows]
    distances = sorted([(distance_squared(a, b), a, b) for a, b in itertools.combinations(rows, 2)])
    # pprint(distances)

    network = {
        net: net_id
        for net_id, net in enumerate(rows)
    }

    for _, a, b in distances:
        new_net_id = network[b]

        for p in network:
            if network[p] == new_net_id:
                network[p] = network[a]
        nets = set(network.values())
        if len(nets) == 1:  # everything is now connected
            return a[0] * b[0]  # this was the last node to get connected
    return 0

if __name__ == "__main__":
    print("part1:", part1())
    print("part2:", part2())

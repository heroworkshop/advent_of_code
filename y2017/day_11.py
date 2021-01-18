from functools import lru_cache

from aocd_tools import load_input_data


DIRECTIONS = {
    "se": (1, 0),
    "nw": (-1, 0),
    "n": (0, -1),
    "s": (0, 1),
    "ne": (1, -1),
    "sw": (-1, 1)
}


def parse(line):
    return DIRECTIONS[line]


def run():
    input_data = load_input_data(2017, 11)
    print(f"loaded input data ({len(input_data)} bytes)")
    lines = [parse(line) for line in input_data.split(",")]
    print("solution1 = ", solution1(lines))
    print("solution2 = ", solution2(lines))


def solution1(moves):
    position = (0, 0)
    for move in moves:
        position = vector_add(position, move)
    return shortest_path_to(position)


def vector_add(va, vb):
    return tuple([a+b for a, b in zip(va, vb)])


@lru_cache(None)
def shortest_path_to(target):
    pos = (0, 0)
    count = 0
    while pos != target:
        if pos[0] < target[0] and pos[1] > target[1]:
            d = "ne"
        elif pos[0] > target[0] and pos[1] < target[1]:
            d = "sw"
        elif pos[0] < target[0]:
            d = "se"
        elif pos[0] > target[0]:
            d = "nw"
        elif pos[1] < target[1]:
            d = "s"
        elif pos[1] > target[1]:
            d = "n"
        else:
            break
        pos = vector_add(pos, DIRECTIONS[d])
        count += 1
    return count


def solution2(moves):
    position = (0, 0)
    furthest = 0
    for move in moves:
        position = vector_add(position, move)
        furthest = max(furthest, shortest_path_to(position))
    return furthest


if __name__ == "__main__":
    run()

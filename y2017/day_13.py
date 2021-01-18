from collections import namedtuple
from contextlib import suppress

from aocd_tools import load_input_data

Layer = namedtuple("layer", "index height")


EXAMPLE = """
0: 3
1: 2
4: 4
6: 4""".strip()


def parse(line):
    index, _, height = line.partition(":")
    return Layer(int(index), int(height))


def run():
    input_data = load_input_data(2017, 13)
    # input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    lines = [parse(line) for line in input_data.split("\n")]
    print("solution1 = ", solution1(lines))
    print("solution2 = ", solution2(lines))


def solution1(lines, p=0):
    layers = {line.index: line.height for line in lines}
    scanners = {index: (0, 1) for index in layers}
    last_layer = max(layers)
    severity = 0

    while p <= last_layer:
        # print(render(layers, scanners, p))
        with suppress(KeyError):
            if scanners[p][0] == 0:
                severity += p * layers[p]
        for index, scanner in scanners.items():
            y, v = scanner
            if y + v >= layers[index] or y + v < 0:
                v = -v
            y += v
            scanners[index] = (y, v)

        p += 1

    return severity


def render(layers, scanners, pos):
    last_layer = max(layers)
    biggest_layer = max(layers.values())

    def header(v):
        return f" {v} " if v != pos else f"({v})"

    result = [" ".join([header(i) for i in range(last_layer)])]
    for row in range(biggest_layer):
        cells = []
        for n in range(last_layer):
            if n in layers:
                if row < layers[n]:
                    scan_char = "S" if scanners[n][0] == row else " "
                    cells.append(f"[{scan_char}]")
                else:
                    cells.append("   ")
            else:
                if row == 0:
                    cells.append("...")
                else:
                    cells.append("   ")
        result.append(" ".join(cells))
    return "\n".join(result)


def solution2(lines):
    p = -1
    while True:
        collision_point = find_collision(lines, p)
        if collision_point == -1:
            return -p
        if p % 1000 == 0:
            print(f"{p} -> {collision_point}")
        p -= 1


def find_collision(lines, p=0):
    layers = {line.index: line.height for line in lines}
    scanners = {index: (0, 1) for index in layers}
    last_layer = max(layers)

    while p <= last_layer:
        # print(render(layers, scanners, p))
        with suppress(KeyError):
            if scanners[p][0] == 0:
                return p
        for index, scanner in scanners.items():
            y, v = scanner
            if y + v >= layers[index] or y + v < 0:
                v = -v
            y += v
            scanners[index] = (y, v)

        p += 1

    return -1


if __name__ == "__main__":
    run()

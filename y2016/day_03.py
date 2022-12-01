from contextlib import suppress

from input_data.day3 import INPUT_DATA


def parse(line):
    return [int(v) for v in line.split()]


def run():
    input_data = convert_from_text(INPUT_DATA)
    print("solution1=", solution1(input_data))
    input_data = convert_from_text(INPUT_DATA)
    print("solution2=", solution2(input_data))


def convert_from_text(input_data):
    return [parse(line) for line in input_data.split("\n")]


def solution1(input_data):
    return count_valid_triangles(input_data)


def count_valid_triangles(input_data):
    count = 0
    for sides in input_data:
        sides.sort()
        if sides[0] + sides[1] > sides[2]:
            count += 1
    return count


def solution2(input_data):
    triangles = extract_as_column_groups(input_data)

    return count_valid_triangles(triangles)


def extract_as_column_groups(input_data):
    rows = iter(input_data)
    triangles = []
    with suppress(StopIteration):
        while True:
            group = [[side] for side in next(rows)]
            for _ in range(2):
                row = next(rows)
                for i, side in enumerate(row):
                    group[i].append(side)
            triangles.extend(group)
    assert len(group[0]) == len(group[1]) == len(group[2]) == 3
    return triangles


if __name__ == "__main__":
    run()

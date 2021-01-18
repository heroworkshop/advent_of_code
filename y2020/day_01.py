from aocd_tools import load_input_data, ints_from_lines


def run():
    input_data = load_input_data(2020, 1)
    print(f"loaded input data ({len(input_data)} bytes)")

    entries = ints_from_lines(input_data)
    print(entries)

    print("solution1 = ", solution1(entries))
    print("solution2 = ", solution2(entries))


def solution1(entries):
    for e in entries:
        if 2020 - e in entries:
            return (2020 - e) * e


def solution2(entries):
    for i, e in enumerate(entries):
        for i2, e2 in enumerate(entries):
            for i3, e3 in enumerate(entries):
                if len({i, i2, i3}) == 3 and e + e2 + e3 == 2020:
                    return e3 * e * e2


if __name__ == "__main__":
    run()
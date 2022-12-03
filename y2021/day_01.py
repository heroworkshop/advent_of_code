from aocd_tools import load_input_data, ints_from_lines


def run():
    input_data = load_input_data(2021, 1)
    print(f"loaded input data ({len(input_data)} bytes)")

    entries = ints_from_lines(input_data)
    # print(entries)

    print("solution1 = ", solution1(entries))
    print("solution2 = ", solution2(entries))


def solution1(entries):
    return sum([
        b > a
        for a, b in zip(entries, entries[1:])
    ])


def solution2(entries):
    return solution1(
        [sum(t) for t in zip(entries, entries[1:], entries[2:])]
    )


if __name__ == "__main__":
    run()

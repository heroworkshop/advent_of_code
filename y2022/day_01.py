from aocd_tools import load_input_data, ints_from_lines


def run():
    input_data = load_input_data(2022, 1)
    print(f"loaded input data ({len(input_data)} bytes)")

    elves = input_data.split("\n\n")
    entries = [sum(ints_from_lines(elf)) for elf in elves]
    print(entries)

    print("solution1 = ", solution1(entries))
    print("solution2 = ", solution2(entries))


def solution1(entries):
    return max(entries)


def solution2(entries):
    return sum(sorted(entries)[-3:])


if __name__ == "__main__":
    run()

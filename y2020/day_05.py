from aocd_tools import load_input_data, ints_from_lines


def run():
    input_data = load_input_data(2020, 5)
    print(f"loaded input data ({len(input_data)} bytes)")

    entries = input_data.split("\n")
    print(entries)

    print("solution1 = ", solution1(entries))
    print("solution2 = ", solution2(entries))


def seat_id(entry):
    lower = 0
    upper = 127
    for v in entry[:7]:
        m = lower + (upper - lower) // 2
        if v == "F":
            upper = m
        elif v == "B":
            lower = m + 1
        print(f"{v} -> ({lower}, {upper})")
    assert lower == upper
    row = lower

    lower = 0
    upper = 7
    for v in entry[-3:]:
        m = lower + (upper - lower) // 2
        if v == "L":
            upper = m
        elif v == "R":
            lower = m + 1
        print(f"{v} -> ({lower}, {upper})")
    assert lower == upper
    col = lower
    print(f"row = {row} column = {col}")
    seat_id = row * 8 + col
    print(f"seat_id = {seat_id}")
    return seat_id


def solution1(entries):
    seat_ids = [seat_id(entry) for entry in entries]
    return max(seat_ids)


def solution2(entries):
    seat_ids = [seat_id(entry) for entry in entries]
    for s in seat_ids:
        if s + 2 in seat_ids and s + 1 not in seat_ids:
            return s + 1
    return None


if __name__ == "__main__":
    run()

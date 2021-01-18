from aocd_tools import load_input_data, ints_from_lines


def run():
    input_data = load_input_data(2019, 1)
    print(f"loaded input data ({len(input_data)} bytes)")

    fuel = [fuel_from_m(m) for m in ints_from_lines(input_data)]
    print("Part 1 answer=", sum(fuel))

    fuel = [total_fuel_from(m) for m in ints_from_lines(input_data)]
    print("Part 2 answer=", sum(fuel))


def fuel_from_m(m):
    return m // 3 - 2


def total_fuel_from(m):
    total = 0
    while True:
        fuel = fuel_from_m(m)
        if fuel < 1:
            break
        total += fuel
        m = fuel
    return total


if __name__ == "__main__":
    run()

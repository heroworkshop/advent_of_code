from functools import partial

from aocd_tools import load_input_data


def spin(row, count):
    result = row[-count:]
    result.extend(row[:-count])
    return result


def exchange(row, a, b):
    row[a], row[b] = row[b], row[a]
    return row


def partner(row, a, b):
    pa = row.index(a)
    pb = row.index(b)
    return exchange(row, pa, pb)


def parse(line):
    op = line[0]
    if op == "s":
        count = int(line[1:])
        return partial(spin, count=count)
    elif op == "x":
        a, b = [int(n) for n in line[1:].split("/")]
        return partial(exchange, a=a, b=b)
    elif op == "p":
        a, b = line[1:].split("/")
        return partial(partner, a=a, b=b)

    return line


def run():
    input_data = load_input_data(2017, 16)
    print(f"loaded input data ({len(input_data)} bytes)")
    operations = [parse(line) for line in input_data.split(",")]
    row = solution1(operations)
    print("solution1 = ", row)
#    print("solution2 = ", solution2(row))
    print("solution2 = ", solution2(operations))


def solution1(operations):
    row = list("abcdefghijklmnop")
    for operation in operations:
        row = operation(row=row)
    return "".join(row)


def solution2(operations):
    initial_row = list("abcdefghijklmnop")

    target_rep = 1000000000
    row, count, cycle_size = run_operations(initial_row, operations, target_rep)
    if count != target_rep:
        row, count, cycle_size = run_operations(row, operations, (target_rep - count) % cycle_size)
    print(f"Ran {count} reps")
    return "".join(row)


def run_operations(initial_row, operations, target_rep):
    row = initial_row
    seen = {tuple(initial_row): 0}
    cycle_size = None
    for i in range(target_rep):
        if i % max(1, target_rep//100) == 0:
            print(".", end="")
        for operation in operations:
            row = operation(row=row)
        # print(i + 1, "".join(row))
        key = tuple(row)
        if tuple(row) in seen:
            cycle_size = i + 1 - seen[key]
            print(i + 1, "".join(row))
            print("last seen ", seen[key])
            print(f"\nFound cycle at {i + 1}")
            break
        seen[tuple(row)] = i
    print()
    return row, i + 1, cycle_size


if __name__ == "__main__":
    run()

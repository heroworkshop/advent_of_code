from aocd_tools import load_input_data


def run():
    input_data = load_input_data(2017, 1)
    print(f"loaded input data ({len(input_data)} bytes)")
    print("solution1 = ", solution1(input_data))
    print("solution2 = ", solution2(input_data))


def solution1(line):
    line += line[0]
    last = int(line[0])
    total = 0
    for ch in line[1:]:
        v = int(ch)
        if v == last:
            total += last
        last = v
    return total


def solution2(line):
    n = len(line)
    offset = n // 2
    line += line
    line += line[0]
    total = 0
    for i in range(n):
        v1 = int(line[i])
        v2 = int(line[i + offset])
        if v1 == v2:
            total += v1
    return total


if __name__ == "__main__":
    run()

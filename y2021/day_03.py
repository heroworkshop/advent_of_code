from collections import Counter

from aocd_tools import load_input_data


def run():
    input_data = load_input_data(2021, 3)
    print(f"loaded input data ({len(input_data)} bytes)")

    entries = parse_cmds(input_data)

    print("solution1 = ", solution1(entries))
    print("solution2 = ", solution2(entries))


def parse_cmds(input_data):
    def parse_line(x):
        return x
    return [parse_line(line) for line in input_data.split("\n")]


def most_common(bit_pos, lines):
    counts = Counter([x[bit_pos] for x in lines])
    return "0" if counts["0"] > counts["1"] else "1"


def least_common(bit_pos, lines):
    counts = Counter([x[bit_pos] for x in lines])
    return "1" if counts["1"] < counts["0"] else "0"


def solution1(lines):
    v_len = len(lines[0])
    gamma = [most_common(i, lines) for i in range(v_len)]
    epsilon = [least_common(i, lines) for i in range(v_len)]
    gamma = int("".join(gamma), 2)
    epsilon = int("".join(epsilon), 2)

    return gamma * epsilon


def freq_reduce(lines, filter_func):
    p = 0
    while len(lines) > 1:
        bit = filter_func(p, lines)
        lines = [line for line in lines if line[p] == bit]
        p += 1
    return int(lines[0], 2)


def solution2(lines):
    o2 = freq_reduce(lines, most_common)
    co2 = freq_reduce(lines, least_common)
    return o2 * co2


if __name__ == "__main__":
    run()

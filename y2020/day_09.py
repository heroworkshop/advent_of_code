from itertools import combinations

from aocd_tools import load_input_data

PREAMBLE = 25

EXAMPLE = """
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576""".strip()

def run():
    input_data = load_input_data(2020, 9)
    # input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    values = [int(x) for x in input_data.split("\n")]
    s1 = solution1(values)
    print("solution1 = ", s1)
    print("solution2 = ", solution2(values, s1))


def solution1(values):
    for n in range(PREAMBLE, len(values)):
        valid = [sum(x) for x in combinations(values[n-PREAMBLE: n], 2)]
        if values[n] not in valid:
            return values[n]
    raise ValueError


def solution2(values, s1):
    for n in range(len(values)):
        total = 0
        dn = 1
        while total < s1:
            try:
                total += values[n + dn]
            except IndexError:
                break
            if total == s1:
                smallest = min(values[n:n+dn])
                largest = max(values[n:n+dn])
                return smallest + largest
            dn += 1

    raise ValueError


if __name__ == "__main__":
    run()

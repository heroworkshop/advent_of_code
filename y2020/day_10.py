from collections import defaultdict

from aocd_tools import load_input_data


EXAMPLE = """
16
10
15
5
1
11
7
19
6
12
4""".strip()

EXAMPLE2 = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3""".strip()

def run():
    input_data = load_input_data(2020, 10)
    # input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    lines = [int(x) for x in input_data.split("\n")]
    print("solution1 = ", solution1(lines))
    print("solution2 = ", solution2(lines))


def solution1(joltages):
    joltages = sorted(joltages)
    print(joltages)
    prev = 0
    diffs = []
    for j in joltages:
        diffs.append(j - prev)
        prev = j
    diffs.append(3)

    delta3_count = len([d for d in diffs if d == 3])
    delta1_count = len([d for d in diffs if d == 1])
    return delta1_count * delta3_count




def solution2(joltages):
    # joltages.append(0)
    joltages = sorted(joltages)
    joltages.append(joltages[-1]+3)
    print(joltages)
    combinations = defaultdict(int, {0: 1})
    for j in joltages:
        combinations[j] = combinations[j - 1] + combinations[j - 2] + combinations[j - 3]
    return combinations[j]


if __name__ == "__main__":
    run()

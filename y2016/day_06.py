from collections import defaultdict

from input_data.day6 import INPUT_DATA


def parse(line):
    return line


def run():
    input_data = [parse(line) for line in INPUT_DATA.split("\n")]
    print("solution1=", solution1(input_data))
    print("solution2=", solution2(input_data))


def solution1(input_data):
    tallies = [defaultdict(int) for _ in range(len(input_data[0]))]
    for line in input_data:
        for i, ch in enumerate(line):
            tallies[i][ch] += 1

    result = [most_frequent(tally) for tally in tallies]

    return "".join(result)


def most_frequent(tally):
    f_max = max(tally.values())
    candidates = [k for k, v in tally.items() if v == f_max]
    candidates.sort()
    return candidates[0]


def least_frequent(tally):
    f_max = min(tally.values())
    candidates = [k for k, v in tally.items() if v == f_max]
    candidates.sort()
    return candidates[0]

def solution2(input_data):
    tallies = [defaultdict(int) for _ in range(len(input_data[0]))]
    for line in input_data:
        for i, ch in enumerate(line):
            tallies[i][ch] += 1

    result = [least_frequent(tally) for tally in tallies]

    return "".join(result)


if __name__ == "__main__":
    run()

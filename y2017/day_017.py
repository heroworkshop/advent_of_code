from collections import deque

from aocd_tools import load_input_data


def parse(line):
    return int(line)


def run():
    input_data = 301

    print("solution1 = ", solution1(input_data))
    print("solution2 = ", solution2(input_data))


def solution1(skip):
    buffer = deque([0])
    p = 0
    for i in range(1, 2018):
        p += skip
        p = p % len(buffer)
        p += 1
        buffer.insert(p, i)
        # print(buffer)
    return buffer[p + 1]


def solution2(lines):
    return


if __name__ == "__main__":
    run()

from collections import deque

from aocd_tools import load_input_data

EXAMPLE = """mjqjpqmgbljsphdztnvjfqwrcgsmlb"""


def run():
    input_data = load_input_data(2022, 6)
    #input_data = EXAMPLE

    print(f"loaded input data ({len(input_data)} bytes)")

    entries = parse(input_data)
    print(entries[:50])

    print("solution1 = ", find_first_unique(entries, 4))
    print("solution2 = ", find_first_unique(entries, 14))


def parse(input_data):
    return input_data


def find_first_unique(entries, length):
    buffer = deque()
    for p, ch in enumerate(entries, 1):
        buffer.append(ch)
        if len(buffer) > length:
            buffer. popleft()
            s = set(buffer)
            if len(s) == length:
                return p
    return None


if __name__ == "__main__":
    run()

from collections import deque

from input_data.day9 import INPUT_DATA


def parse(line):
    return int(line)


def run():
    input_data = INPUT_DATA
    print("solution1=", solution1(input_data))
    print("solution2=", solution2(input_data))


def solution1(input_data):
    return len(parse(input_data))


def parse(input_data):
    result = ""
    p = 0
    while p < len(input_data):
        if input_data[p] == "(":
            decompressed, p = decompress(input_data, p)
        else:
            decompressed = input_data[p]
            p += 1
        result += decompressed
    return result


def parse_counter(input_data):
    count = 0
    p = 0
    while p < len(input_data):
        if input_data[p] == "(":
            decompressed_count, p = decompress_counter(input_data, p)
        else:
            decompressed_count = 1
            p += 1
        count += decompressed_count
    return count


def decompress(input_data, p_start):
    p_end = input_data.index(")", p_start)
    instruction = input_data[p_start + 1: p_end]
    length, _, count = instruction.partition("x")
    length, count = int(length), int(count)
    block = input_data[p_end + 1: p_end + 1 + length]
    decompressed = block * count
    print(f"{length} x {count} -> {decompressed}")
    return decompressed, p_end + length + 1

def decompress_counter(input_data, p_start):
    p_end = input_data.index(")", p_start)
    instruction = input_data[p_start + 1: p_end]
    length, _, count = instruction.partition("x")
    length, count = int(length), int(count)
    block = input_data[p_end + 1: p_end + 1 + length]
    decompressed = parse_counter(block) * count
    print(f"{length} x {count} -> {decompressed}")
    return decompressed, p_end + length + 1


def solution2(input_data):
    return parse_counter(input_data)


if __name__ == "__main__":
    run()

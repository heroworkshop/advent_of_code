from collections import defaultdict, namedtuple, deque
from functools import lru_cache
from hashlib import md5

from aocd_tools import load_input_data

INPUT_DATA = b"jlmsuwbz"


def parse(line):
    return line


def run():
    # print("solution1 = ", solution1())
    print("solution2 = ", solution2())


@lru_cache(1500)
def make_hash(index, salt=INPUT_DATA):
    return md5(INPUT_DATA + f"{index}".encode('utf-8')).hexdigest()


@lru_cache(1500)
def make_stretched_hash(index, salt=INPUT_DATA):
    next_hash = make_hash(index, salt)
    for _ in range(2016):
        next_hash = md5(next_hash.encode()).hexdigest()
    return next_hash


def find_first_repeat(hash_str, n):
    buf = deque(hash_str[:n - 1])
    for ch in hash_str[n - 1:]:
        buf.append(ch)
        if len(set(buf)) == 1:
            return buf[0]
        buf.popleft()
    raise ValueError


def is_valid(hash_val, i, hasher=make_hash):
    try:
        ch = find_first_repeat(hash_val, 3)
        # print("Found ", ch * 3, f"at index {i}")
    except ValueError:
        return False
    for di in range(1, 1001):
        if ch * 5 in hasher(di + i):
            # print("Found ", ch * 5, f"at index {i + di}")
            return True
    # print("Couldn't find ", ch * 5, f" in next 1000")
    return False


def solution1():
    one_time_pad = []
    i = 0
    while len(one_time_pad) < 64:
        hashed = make_hash(i)
        if is_valid(hashed, i):
            one_time_pad.append(hashed)
            print(f"key {len(one_time_pad)} produced")
        i += 1

    return i - 1


def solution2():
    one_time_pad = []
    i = 0
    while len(one_time_pad) < 64:
        hashed = make_stretched_hash(i)
        if is_valid(hashed, i, make_stretched_hash):
            one_time_pad.append(hashed)
            print(f"key {len(one_time_pad)} produced")
        i += 1

    return i - 1


if __name__ == "__main__":
    run()

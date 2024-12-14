import re
from contextlib import suppress
from functools import cache

from aocd_tools import *


EXAMPLE = """125 17"""

def run():
    input_data = load_input_data()
    # input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    entries = [int(s) for s in input_data.split()]

    print(entries)

    for i, f in enumerate((solution1, solution2), 1):
        start_time = time.process_time()
        print(f"solution{i} = ", f(entries), time_report(start_time))



def solution1(entries):
    stones = entries
    for i in range(25):
        stones = update(stones)
        print(f"{i+1}: {len(stones)} stones")
        if len(stones) <10:
            print(stones)
    return len(stones)

def solution2(entries):
    return sum(solve(s, 75) for s in entries)


@cache
def solve(stone, n):
    if n == 0:
        return 1
    while n:
        s = str(stone)
        if stone == 0:
            stone = 1
            n -= 1
        elif len(s) % 2 != 0:
            stone *= 2024
            n -= 1
        else:
            a = int(s[:len(s)//2])
            b = int(s[len(s)//2:])
            return solve(a, n-1) + solve(b, n-1)
    return 1


def update(stones):
    new_stones = []
    for stone in stones:
        s = str(stone)
        if stone == 0:
            new_stones.append(1)
        elif len(s) % 2 == 0:
            new_stones.append(int(s[:len(s)//2]))
            new_stones.append(int(s[len(s)//2:]))
        else:
            new_stones.append(stone * 2024)
    return new_stones

    return new_stones



if __name__ == "__main__":
    run()

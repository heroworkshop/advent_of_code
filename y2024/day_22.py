import re
from aocd_tools import *


EXAMPLE = """1
10
100
2024"""

def run():
    input_data = load_input_data()
    # input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    entries = [process_one_line(line) for line in input_data.splitlines()]

    print(entries)

    for i, f in enumerate((solution1, solution2), 1):
        start_time = time.process_time()
        print(f"solution{i} = ", f(entries), time_report(start_time))


def process_one_line(line):
    return int(line)


def solution1(entries):
    total = 0
    for secret in entries:
        # print(secret, end=": ")
        for _ in range(2000):
            secret = next_secret(secret)
        # print(secret)
        total += secret
    return total


def solution2(entries):
    price_tables = []
    best = 0
    for secret0 in entries:
        price_table = make_price_table(secret0, 2000)
        price_tables.append(price_table)

    for i, price_table in enumerate(price_tables):
        print(f"{i:04}", end=": ")
        for j, diff in enumerate(price_table):
            total = sum(table.get(diff, 0) for table in price_tables)
            best = max(best, total)
            if j % 20 == 0:
                print(".", end="")
        print(best)

    return best


def make_price_table(secret, n):
    price_table = {}
    diffs = get_digits(n, secret)
    for i, (price, diff) in enumerate(diffs[3:], 3):
        diff_match = tuple(diffs[i - 3 + j][1] for j in range(4))
        if diff_match not in price_table:
            price_table[diff_match] = price
    return price_table


def get_digits(n, secret):
    diffs = []
    digit0 = secret % 10
    for _ in range(n):
        secret = next_secret(secret)
        digit = secret % 10
        diffs.append((digit, (digit - digit0)))
        digit0 = digit
    return diffs

def nth_secret(secret, n):
    for _ in range(n):
        secret = next_secret(secret)
    return secret

def extract_lines(entries):
    return entries.split("\n")


def mix(secret, n):
    return secret ^ n


def prune(n):
    return n % 16777216


def next_secret(secret):
    # Calculate the result of multiplying the secret number by 64. Then, mix this result into the secret number. Finally, prune the secret number.
    secret = mix(secret, secret * 64)
    secret = prune(secret)
    # Calculate the result of dividing the secret number by 32. Round the result down to the nearest integer.
    # Then, mix this result into the secret number. Finally, prune the secret number.
    secret = mix(secret, secret // 32)
    secret = prune(secret)
    # Calculate the result of multiplying the secret number by 2048.
    # Then, mix this result into the secret number. Finally, prune the secret number.
    secret = mix(secret, secret * 2048)
    secret = prune(secret)
    return secret

if __name__ == "__main__":
    run()

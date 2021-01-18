from collections import namedtuple

from aocd_tools import load_input_data, ints_from_lines

Password = namedtuple("password", "min max ch pwd")


def make_password(line):
    e = line.split(" ")
    min_count, _, max_count = e[0].partition("-")
    ch, _, _ = e[1].partition(":")
    return Password(int(min_count), int(max_count), ch, e[2])


def run():
    input_data = load_input_data(2020, 2)
    print(f"loaded input data ({len(input_data)} bytes)")

    entries = [make_password(line) for line in input_data.split("\n")]
    print(entries)

    print("solution1 = ", solution1(entries))
    print("solution2 = ", solution2(entries))


def is_valid(password):
    n = password.pwd.count(password.ch)
    return password.min <= n <= password.max


def is_valid2(password):
    v = password.pwd[password.min - 1] + password.pwd[password.max - 1]
    return v.count(password.ch) == 1


def solution1(entries):
    valid_passwords = [e.pwd for e in entries if is_valid(e)]
    return len(valid_passwords)


def solution2(entries):
    valid_passwords = [e.pwd for e in entries if is_valid2(e)]
    return len(valid_passwords)


if __name__ == "__main__":
    run()

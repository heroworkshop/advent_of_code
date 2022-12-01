from collections import namedtuple

from input_data.day7 import INPUT_DATA

Ipv7 = namedtuple("ipv7", "supernet hypernet")


def parse(line):
    line = line.replace("]", "[")

    parts = line.split("[")
    supernet = parts[::2]
    hypernet = parts[1::2]
    return Ipv7(supernet, hypernet)


def run():
    input_data = [parse(line) for line in INPUT_DATA.split("\n")]
    print("solution1=", solution1(input_data))
    print("solution2=", solution2(input_data))


def solution1(input_data):
    return len([line for line in input_data if supports_tls(line)])


def supports_tls(parts):
    if any([contains_abba(p) for p in parts.hypernet]):
        return False
    return any([contains_abba(p) for p in parts.supernet])


def contains_abba(s):
    for p in range(len(s) - 3):
        front = s[p:p + 2]
        back = s[p + 3: p + 1: -1]
        if front == back and s[p] != s[p + 1]:
            return True
    return False


def supports_ssl(parts):
    for aba in find_aba(" ".join(parts.hypernet)):
        bab = aba[1] + aba[0] + aba[1]
        if bab in " ".join(parts.supernet):
            return True


def find_aba(s):
    return [s[p: p + 3] for p in range(len(s) - 2)
            if s[p] == s[p + 2] and s[p] != s[p + 1]]


def solution2(input_data):
    return len([line for line in input_data if supports_ssl(line)])


if __name__ == "__main__":
    run()

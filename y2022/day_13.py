import json
from collections import deque
from dataclasses import dataclass
from functools import cmp_to_key
from pprint import pprint
from typing import NamedTuple, List

from aocd_tools import load_input_data

EXAMPLE = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""


EX2 = """[1, [1, 2], 2]
[1, [1, 2], 1]"""

class Packet(NamedTuple):
    left: List
    right: List

def run():
    input_data = load_input_data(2022, 13)  # >705
    # input_data = EXAMPLE
    # input_data = EX2

    print(f"loaded input data ({len(input_data)} bytes)")

    entries = input_data.split("\n\n")
    entries = [parse(line) for line in entries]
    pprint(entries[:50])

    print("solution1 = ", solution1(entries))

    flat_list = [item for item in input_data.split("\n") if len(item)]
    print("solution2 = ", solution2(flat_list))


def packet_compare(packet: Packet):
    assert isinstance(packet.left, list)
    assert isinstance(packet.right, list)

    for left, right in zip(packet.left, packet.right):
        if isinstance(left, list) or isinstance(right, list):
            c = packet_compare(Packet(ensure_list(left), ensure_list(right)))
            if c is not None:
                return c
        else:
            if right < left:
                return False
            if left < right:
                return True
    if len(packet.right) < len(packet.left):
        return False
    if len(packet.right) > len(packet.left):
        return True
    return None


def ensure_list(v):
    return v if isinstance(v, list) else [v]


def parse(line: str):
    return Packet(*(json.loads(packet) for packet in line.split("\n")))


def solution1(entries):
    correct_packets = [i for i, packet in enumerate(entries, 1) if packet_compare(packet)]
    return sum(correct_packets)


def solution2(entries):
    dividers = ["[[2]]", "[[6]]"]
    def compare(a, b):
        packet = Packet(json.loads(a), json.loads(b))
        if packet_compare(packet):
            return -1
        else:
            return 1
    entries.extend(dividers)
    s = sorted(entries, key=cmp_to_key(compare))
    i, j = [s.index(d) + 1 for d in dividers]
    print(i, j)
    return i * j




if __name__ == "__main__":
    run()

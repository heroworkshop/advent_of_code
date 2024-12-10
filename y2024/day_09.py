import re
from aocd_tools import *

EXAMPLE = """2333133121414131402"""


def run():
    input_data = load_input_data()
    # input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    # entries = int_tuples_from_lines(lines=input_data, sep=" ")
    # a, b = entries.split("\n\n")
    # entries = [process_one_line(line) for line in input_data.splitlines()]

    # print(entries)
    print(input_data[:20], "...", input_data[-20:])
    entries = extract(input_data)
    for i, f in enumerate((solution1, solution1b, solution2), 1):
        start_time = time.process_time()
        print(f"solution{i} = ", f(entries), time_report(start_time))


def extract(input_data):
    return input_data[::2], input_data[1::2]

def process_one_line(line):
    return line


def solution1(entries):
    print(len(entries[0]))
    print(len(entries[1]))
    print(entries[0][:20],"...",entries[0][-20:])
    print(entries[1][:20],"...",entries[1][-20:])
    mem = []
    i = 0
    for a, b in zip(*entries):
        mem.extend([i] * int(a))
        mem.extend([None] * int(b))
        # print(a, b, show(mem))
        i += 1
    mem.extend([i] * int(entries[0][-1]))
    # print(show(mem))
    print("mem used=", len(mem))
    p0 = 0
    p1 = len(mem) - 1
    # print(p1)
    total = 0
    while p0 < p1 or mem[p0] is not None:
        if mem[p0] is None:
            while mem[p1] is None:
                p1 -= 1
            total += mem[p1] * p0
            # print(f"{mem[p1]} * {p0}")
            mem[p1] = None
            p1 -= 1
        else:
            total += mem[p0] * p0
            # print(f"{mem[p0]} * {p0}")
        p0 += 1
        # print(p0, p1, mem[p0], mem[p1])
    return total


def solution1b(entries):
    # print(len(entries[0]))
    # print(len(entries[1]))
    # print(entries[0][:20],"...",entries[0][-20:])
    # print(entries[1][:20],"...",entries[1][-20:])
    mem = []
    i = 0
    for a, b in zip(*entries):
        mem.extend([i] * int(a))
        mem.extend([None] * int(b))
        # print(a, b, show(mem))
        i += 1
    mem.extend([i] * int(entries[0][-1]))
    # print(show(mem))
    # print("mem used=", len(mem))
    p0 = 0
    p1 = len(mem) - 1
    # print(p1)
    while p0 < len(mem) and p0 < p1:
        if mem[p0] is None:
            while mem[p1] is None and p0 < p1 -1:
                p1 -= 1
            # print(f"{mem[p1]} * {p0}")
            mem[p0] = mem[p1]
            mem[p1] = None
            p1 -= 1
        p0 += 1
        # print(p0, p1, show(mem))
        # print(p0, p1, mem[p0], mem[p1])
    # print(show(mem))
    total2 = 0
    for p, v in enumerate(mem):
        if v is None:
            break
        total2 += p * v
        # print(f"{p} * {v} = {p*v}")
    return total2


def show(m):
    r = [("." if x is None else str(x)) for x in m]
    return "".join(r)


class Node(NamedTuple):
    count: int
    file_id: int
    gap: int

def solution2(entries):
    count, gaps = entries
    gaps += "0"
    nodes = [Node(int(a), i, int(b)) for i, (a, b) in enumerate(zip(count, gaps))]
    # print(nodes)
    p = -1
    while -p < len(nodes):
        # print(show(nodes_to_mem(nodes)))
        # try:
        block_size = nodes[p].count
        # except IndexError:
        #     break
        for p_to, block_to in enumerate(nodes[:p]):
            if block_to.gap >= block_size:
                new_gap = block_to.gap - block_size
                nodes[p_to] = Node(block_to.count, block_to.file_id, 0)
                nodes.insert(p_to + 1, Node(block_size, nodes[p].file_id, new_gap))
                nodes[p-1] = Node(nodes[p-1].count, nodes[p-1].file_id, nodes[p-1].gap + block_size + nodes[p].gap)
                del nodes[p]
                break
        else:
            p -= 1
        # print(nodes)
    mem = nodes_to_mem(nodes)

    total = 0
    for p, v in enumerate(mem):
        if v:
            total += p * v
    return total


def nodes_to_mem(nodes):
    mem = []
    for node in nodes:
        for _ in range(node.count):
            mem.append(node.file_id)
        mem.extend([None] * node.gap)
    return mem



def extract_lines(entries):
    return entries.split("\n")


if __name__ == "__main__":
    run()

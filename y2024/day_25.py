import re
from aocd_tools import *


EXAMPLE = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""

def run():
    input_data = load_input_data()
    # input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    entries = [grid_from_lines(section, default_val=".") for section in input_data.split("\n\n")]


    for i, f in enumerate((solution1, solution2), 1):
        start_time = time.process_time()
        print(f"solution{i} = ", f(entries), f"  ({time_report(start_time)} s)")


def process_one_line(line):
    return line

def solution1(entries):
    count = 0
    keys, locks = get_keys_and_locks(entries)
    print(f"keys: {len(keys)}, locks: {len(locks)}")
    perfect_match = {
        (x, y) for x in range(5) for y in range(7)
    }
    print(render(perfect_match))
    for k, key in enumerate(keys):
        for l, lock in enumerate(locks):
            if not key.intersection(lock): # and key.union(lock) == perfect_match:
                print(f"match for key {k} and lock {l}")
                print("Lock\n", render(lock), "\nKey\n", render(key))
                count += 1
            else:
                print(f"no match for key {k} and lock {l}")

    return count

def render(s: set):
    lines = []
    for y in range(7):
        line = ""
        for x in range(5):
            line += "#" if (x, y) in s else "."
        lines.append(line)
    return "\n".join(lines)



def solution2(entries):
    return 0

def get_keys_and_locks(entries) -> tuple[list[set], list[set]]:
    keys = []
    locks = []
    for entry in entries:
        for x in range(entry.width):
            if (x,0) not in entry.grid:
                keys.append(set(entry.grid.keys()))
                break
        locks.append(set(entry.grid.keys()))
    return keys, locks

def extract_lines(entries):
    return entries.split("\n")


if __name__ == "__main__":
    run()

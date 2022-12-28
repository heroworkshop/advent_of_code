import time
from collections import deque
from dataclasses import dataclass
from typing import NamedTuple, List, Set

from aocd_tools import load_input_data, Pos

EXAMPLE = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"""

ROCKS = """####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##"""

Shape = List[int]


class GroundedBlocks:
    def __init__(self, buffer_size=10):
        self.buffer_size = buffer_size
        self.rows = [0 for _ in range(self.buffer_size)]
        self.top = -1

    def add(self, shape: Shape, x: int=0):
        for row in reversed(shape):
            self.top += 1
            self.rows[self.top % self.buffer_size] = (row << x)

    def overlaps(self, p: Pos, bits: int):
        if p.y <= self.top - self.buffer_size:
            raise RuntimeError(f"row data at y={p.y} has been discarded due to a buffer size of {self.buffer_size}")
        if p.y > self.top:
            return False

        row = self.rows[p.y % self.buffer_size]
        return (bits << p.x) & row

    def render(self):
        bottom = max(0, self.top - self.buffer_size)
        for y in range(self.top, bottom):
            bits = bin(self.rows[y % self.buffer_size]).replace("0", ".").replace("1", "#")
            print(f"{y:5} |{bits:.>7}|")
        print()

def run():
    input_data = load_input_data(2022, 17)
    # input_data = EXAMPLE

    rocks = [make_rock_prefab(entry) for entry in ROCKS.split("\n\n")]
    print(rocks)
    print(f"loaded input data ({len(input_data)} bytes)")

    t = time.process_time()
    print("solution1 = ", solution1(input_data, rocks))
    dt = get_elapsed(t)
    print(f"in {dt}")


    t = time.process_time()
    print("solution2 = ", solution2(input_data, rocks))
    dt = get_elapsed(t)
    print(f"in {dt}")


    # rocks = [make_rock_prefab_bits(entry) for entry in ROCKS.split("\n\n")]
    # print(rocks)
    # t = time.process_time()
    # print("solution2 = ", solution2(input_data, rocks))
    # dt = get_elapsed(t)
    # print(f"in {dt}")


def get_elapsed(start_t):
    t = time.process_time() - start_t
    if t < 0:
        return f"{t * 1000:.3} ms"
    if t > 120:
        return f"{t / 60:.3} mins"
    return f"{t:.3} s"


def make_rock_prefab(entry: str):
    rock = set()
    rows = entry.split("\n")
    y = len(rows) - 1
    for row in rows:
        for x, ch in enumerate(row):
            if ch == "#":
                rock.add(Pos(x, y))
        y -= 1
    return rock


def make_rock_prefab_bits(entry: str) -> Shape:
    def str_to_bin(s):
        s = s.replace(".", "0").replace("#", "1")
        return "".join(reversed(s))
    return [int(str_to_bin(row), 2) for row in entry.split("\n")]


def solution1(jets, rock_prefabs):
    jet_i = 0
    top = 0
    grounded = set()

    for rock_i, _ in enumerate(range(2022)):
        pos = Pos(2, top + 3)
        rock = make_rock(pos, rock_prefabs, rock_i)
        while True:
            # jet of gas
            dx = -1 if jets[jet_i % len(jets)] == "<" else 1
            jet_i += 1
            new_rock = update_rock(Pos(dx, 0), rock)
            if valid(new_rock, grounded):
                rock = new_rock
            # gravity
            new_rock = update_rock(Pos(0, -1), rock)
            if valid(new_rock, grounded):
                rock = new_rock
            else:
                grounded.update(rock)
                break
        top = max({p.y for p in grounded}) + 1
    return top


def grounded_state(grounded: Set, pos:Pos):
    result = []
    for y in range(pos.y, pos.y - 10, -1):
        b = sum(1 << x for x in range(7) if Pos(x, y) in grounded)
        result.append(b)
    return tuple(result)


def tidy_grounded(grounded: Set, top: int):
    discard = set()
    for p in grounded:
        if p.y < top - 11:
            discard.add(p)
    grounded.difference_update(discard)


def solution2(jets, rock_prefabs):
    rock_i = 0
    jet_i = 0
    top = 0
    grounded = set()
    seen = {}
    extra_blocks = 0

    remaining = 1000000000000
    while remaining:
        if remaining % 1000 == 0:
            print(remaining)
        pos = Pos(2, top + 3)
        rock = make_rock(pos, rock_prefabs, rock_i)
        rock_i += 1
        state = rock_i, jet_i, grounded_state(grounded, pos)
        if state in seen:
            print(f"repeat found at {remaining}")
            prev_remaining, prev_top = seen[state]
            diff = remaining - prev_remaining

            while remaining > diff:
                remaining -= diff
                extra_blocks += top - prev_top
        seen[state] = remaining, top

        while True:
            # jet of gas
            dx = -1 if jets[jet_i % len(jets)] == "<" else 1
            jet_i += 1
            new_rock = update_rock(Pos(dx, 0), rock)
            if valid(new_rock, grounded):
                rock = new_rock
            # gravity
            new_rock = update_rock(Pos(0, -1), rock)
            if valid(new_rock, grounded):
                rock = new_rock
            else:
                grounded.update(rock)
                break
        top = max({p.y for p in grounded}) + 1
        remaining -= 1
        tidy_grounded(grounded, top)
        # render(grounded, top)
    return top


def render(blocks, top):
    for y in range(top + 3, -1, -1):
        row = ""
        for x in range(7):
            row += "#" if (x, y) in blocks else "."
        print(f"|{row}|")
    print("+-------+")



def make_rock(pos, prefabs, i):
    prefab = prefabs[i % len(prefabs)]
    return {pos + p for p in prefab}


def make_rock_bits(prefabs, i):
    prefab = prefabs[i % len(prefabs)]
    return prefab[:]


def update_rock(vect, rock):
    return {p + vect for p in rock}


def valid(rock, grounded):
    if rock.intersection(grounded):
        return False
    y_vals = set(p.y for p in rock)
    if min(y_vals) < 0:
        return False
    x_vals = set(p.x for p in rock)
    if min(x_vals) < 0:
        return False
    if max(x_vals) > 6:
        return False
    return True

def valid_bits(pos: Pos, rock: Shape, grounded: GroundedBlocks):
    y_top = pos.y + len(rock) - 1
    for dy, row in enumerate(rock):
        y = y_top - dy
        if pos.x < 0:
            r = row >> abs(pos.x)
            if r << abs(pos.x) != row:  # check left edge
                return False
        if pos.x > 0:
            r = row << pos.x
            if r > 0b1111111:  # check right edge
                return False
        if y < 0:
            return False
        if y > grounded.top:
            continue
        if grounded.overlaps(Pos(pos.x, y), row):
            return False
    return True


def solution2_bits(jets, rock_prefabs):
    rock_i = 0
    jet_i = 0
    grounded = GroundedBlocks()

    for count in range(2022):
        pos = Pos(2, grounded.top + 3)
        rock = make_rock_bits(rock_prefabs, rock_i)
        rock_i += 1
        while True:
            # jet of gas
            dx = -1 if jets[jet_i % len(jets)] == "<" else 1
            jet_i += 1
            new_pos = pos + Pos(dx, 0)
            if valid_bits(new_pos, rock, grounded):
                pos = new_pos
            # gravity
            new_pos = pos + Pos(0, -1)
            if valid_bits(new_pos, rock, grounded):
                pos = new_pos
            else:
                grounded.add(rock)
                break
        grounded.render()
    return grounded.top + 1


if __name__ == "__main__":
    run()

from collections import deque
from typing import List

from aocd_tools import load_input_data, Pos
from y2022.day_17 import make_rock_bits, make_rock_prefab_bits, EXAMPLE, ROCKS

Shape = List[int]


class GroundedBlocks:
    def __init__(self):
        self.rows = {}
        self.top_y = -1
        self.buffer_size = 50

    def state(self):
        return tuple(self.rows.get(i, 0) for i in range(self.top_y, self.top_y - self.buffer_size, -1))

    def add(self, shape: Shape, p: Pos):
        y = p.y
        for row in reversed(shape):
            self.rows[y] = self.rows.get(y, 0) | (row << p.x)
            self.top_y = max(y, self.top_y)
            if y - self.buffer_size in self.rows:
                del self.rows[y - self.buffer_size]
            y += 1

    def overlaps(self, p: Pos, bits: int):
        if p.y > self.top_y:
            return False
        if p.y not in self.rows:
            raise RuntimeError(f"row data at y={p.y} has been discarded due to a buffer size of {self.buffer_size}")
        return (bits << p.x) & self.rows[p.y]

    def render(self):
        rows = []
        y0 = max(0, self.top_y - self.buffer_size)
        for y in range(self.top_y, y0 - 1, -1):
            v = self.rows.get(y, 0)
            s = f"{v:>07b}".replace("0", ".").replace("1", "#")
            rows.append(f"|{s[::-1]}|")
        rows.append("-" * 9)
        return "\n".join(rows)


def run():
    input_data = load_input_data(2022, 17)
    # input_data = EXAMPLE

    rock_prefabs = [make_rock_prefab_bits(entry) for entry in ROCKS.split("\n\n")]
    print(rock_prefabs)
    jets = input_data

    rock_i = 0
    jet_i = 0
    grounded = GroundedBlocks()
    target = 1000000000000
    seen = {}

    count = 0
    extra_y = 0
    while count != target:
        if count % 10000 == 0:
            print(count)
        pos = Pos(2, grounded.top_y + 4)
        rock = make_rock_bits(rock_prefabs, rock_i)
        rock_i += 1
        count += 1

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
                grounded.add(rock, pos)
                break
        state = rock_i % len(ROCKS), jet_i % len(jets), grounded.state()
        # print(state)
        if not extra_y and state in seen:
            prev_y, prev_count = seen[state]
            print(f"repeat at {count}  y={grounded.top_y} with {len(seen)} unique states")
            print(f"prev count={prev_count}, y={prev_y}")
            dy = grounded.top_y - prev_y
            d_count = count - prev_count
            extra_steps = (target - count) // d_count
            print(f"adding {extra_steps} extra steps")
            count += extra_steps * d_count
            print(f"count now at {count}")
            extra_y += extra_steps * dy
            print(f"Extra height = {extra_y}")
        seen[state] = (grounded.top_y, count)
        # print(grounded.top_y)
        # print(grounded.render(),"\n")
    return grounded.top_y + 1 + extra_y


def valid_bits(pos: Pos, rock: Shape, grounded: GroundedBlocks):
    if pos.x < 0:  # check left edge
        return False
    y_top = pos.y + len(rock) - 1
    for dy, row in enumerate(rock):
        y = y_top - dy
        if pos.x > 0:
            r = row << pos.x
            if r > 0b1111111:  # check right edge
                return False
        if y < 0:
            return False
        if y > grounded.top_y:
            continue
        if grounded.overlaps(Pos(pos.x, y), row):
            return False
    return True


if __name__ == "__main__":
    print("solution=", run())

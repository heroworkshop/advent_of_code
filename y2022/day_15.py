from collections import deque
from dataclasses import dataclass
from typing import NamedTuple, List

from aocd_tools import load_input_data, Pos

EXAMPLE = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""


@dataclass
class Sensor:
    pos: Pos
    closest: Pos
    r: int = 0

    def __post_init__(self):
        self.r = manhatten(self.pos, self.closest)


def run():
    input_data = load_input_data(2022, 15)
    y = 2000000
    # input_data = EXAMPLE; y = 10

    print(f"loaded input data ({len(input_data)} bytes)")

    entries = input_data.split("\n")
    entries = [parse(line) for line in entries]
    print(entries[:50])

    print("solution1 = ", solution1(entries, y))

    print("solution2 = ", solution2(entries, 4000000))


def parse(line: str):
    def int_from_eq(v: str):
        _, _, s = v.partition("=")
        s = s.replace(",", "")
        s = s.replace(":", "")
        return int(s)

    parts = [int_from_eq(p) for p in line.split() if "=" in p]
    return Sensor(Pos(parts[0], parts[1]), Pos(parts[2], parts[3]))


def solution1(entries: List[Sensor], y: int):
    clear = set()
    found = set()
    for sensor in entries:
        if sensor.closest.y == y:
            found.add(sensor.closest.x)
        dy = abs(sensor.pos.y - y)
        # print(f"\n[{sensor.pos.x}, {sensor.pos.y}]: ", end="")
        if sensor.r < dy:
            continue
        lower = sensor.pos.x - (sensor.r - dy)
        upper = sensor.pos.x + (sensor.r - dy)
        for x in range(lower, upper + 1):
            clear.add(x)
            # print(f"{a} {b} ", end="")
    # print("\n", sorted(list(clear)))
    return len(clear) - len(found)


def manhatten(p1: Pos, p2: Pos):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def solution2(entries, size):
    pc10 = size // 10
    progress_interval = size // 200
    for y in range(0, size + 1):
        if y % pc10 == 0:
            print(f"\n{y*100//size:0}% ", end="")
        if y % progress_interval == 0:
            print("#", end="")

        free_x = find_free(entries, y, size)
        if free_x:
            print("\n", free_x)
            x = list(free_x).pop()
            print(f"found at {x}, {y}")
            return x * 4000000 + y
    return


@dataclass
class Span:
    lower: int
    upper: int


def find_free(entries, y, max_x):
    low_x = 0
    high_x = max_x
    spans = []
    for sensor in entries:
        dy = abs(sensor.pos.y - y)
        # print(f"\n[{sensor.pos.x}, {sensor.pos.y}]: ", end="")
        if sensor.r < dy:
            continue
        lower = max(low_x, sensor.pos.x - (sensor.r - dy))
        upper = min(high_x, sensor.pos.x + (sensor.r - dy))
        combine_spans(spans, lower, upper)

    # print("All sensors considered. Consolidating spans...")
    while True:
        count = len(spans)
        final_span = [spans.pop()]
        # print(final_span)
        for span in spans:
            combine_spans(final_span, span.lower, span.upper)
        if len(final_span) == count:
            break
        spans = final_span

    if len(final_span) == 1:
        return

    clear = set(range(max_x + 1))
    for span in final_span:
        for x in range(span.lower, span.upper + 1):
            clear.discard(x)
    return clear


def combine_spans(spans: List[Span], lower: int, upper: int):
    # print(f"  adding ({lower} to {upper})")
    overlap = False
    for span in spans:
        if (lower <= span.upper <= upper) or (upper >= span.lower >= lower):
            hi = max(upper, span.upper)
            low = min(lower, span.lower)
            span.upper = hi
            upper = hi
            span.lower = low
            lower = low
            overlap = True
    if not overlap:
        spans.append(Span(lower, upper))
    # print("  ", spans)


if __name__ == "__main__":
    run()

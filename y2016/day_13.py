import heapq
import math
from collections import defaultdict, namedtuple


from aocd_tools import load_input_data, Grid

EXAMPLE = """"""

N = 1362


def parse(line):
    return line


def run():
    print("solution1 = ", solution1())
    print("solution2 = ", solution2())


def is_wall(pos):
    x, y = pos
    v = x*x + 3*x + 2*x*y + y + y*y + N
    binv = f"{v:b}"
    return bool(binv.count("1") % 2)


def all_valid_neighbours(p):
    x, y = p
    return [
        (x + dx, y + dy)
        for dx, dy in [(0, -1), (-1, 0), (1, 0), (0, 1)]
        if x + dx >= 0 and y + dy >= 0 and not is_wall((x + dx, y + dy))
    ]


def render_grid_point(ch):
    if ch == math.inf:
        return "."
    return str(min(ch//1, 9))


def solution1():
    queue = []
    visited = Grid(default_val=math.inf)
    target = 31, 39

    def add_to_queue(p, steps):
        x, y = p
        tx, ty = target
        manhatten_distance = abs(tx - x) + abs(ty - y)
        heapq.heappush(queue, (manhatten_distance, steps, p))

    add_to_queue((1, 1), 0)

    best_path = math.inf

    while queue:
        dist, steps, p = heapq.heappop(queue)
        if steps > best_path:
            continue
        if p in visited.grid and steps >= visited.at(p):
            continue
        if p == target:
            if steps < best_path:
                best_path = steps
            print(f"Found new route using {steps} steps")
        visited.add(p, steps)
        for neighbour in all_valid_neighbours(p):
            add_to_queue(neighbour, steps + 1)

        print(visited.render(render_char=render_grid_point), "\n")

    return best_path



def solution2():
    queue = []
    visited = Grid(default_val=math.inf)

    def add_to_queue(p, steps):
        heapq.heappush(queue, (steps, p))

    add_to_queue((1, 1), 0)

    while queue:
        steps, p = heapq.heappop(queue)
        if steps > 50:
            continue
        if p in visited.grid and steps >= visited.at(p):
            continue

        visited.add(p, steps)
        for neighbour in all_valid_neighbours(p):
            add_to_queue(neighbour, steps + 1)

        # print(visited.render(render_char=render_grid_point), "\n")

    return len([x for x in visited.grid if x != math.inf])




if __name__ == "__main__":
    run()

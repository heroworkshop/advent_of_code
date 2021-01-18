import copy
from collections import defaultdict

from aocd_tools import load_input_data, grid_from_lines


EXAMPLE = """
#########
#G.#G..G#
#..##...#
#.......#
#G..E..G#
#.......#
#.......#
#G..G..G#
#########""".strip()

INFINITY = 999999999


class Actor:
    def __init__(self, pos, symbol):
        self.pos = pos
        self.symbol = symbol
        self.distance_graph = defaultdict(lambda: INFINITY)

    def compute_distances(self, grid):
        nodes = [self.pos]
        self.distance_graph[self.pos] = 0
        while nodes:
            x, y = nodes.pop(0)
            d = self.distance_graph[(x, y)] + 1
            for np in (
                    (x + 1, y),
                    (x - 1, y),
                    (x, y + 1),
                    (x, y - 1)
            ):
                if grid.at(np) != "#" and d < self.distance_graph[np]:
                    self.distance_graph[np] = d
                    nodes.append(np)


def extract_actors(grid, symbols):
    actors = []
    for y in range(grid.y_bounds.min, grid.y_bounds.max + 1):
        for x in range(grid.x_bounds.min, grid.x_bounds.max + 1):
            s = grid.at((x, y))
            if s in symbols:
                a = Actor((x, y), s)
                a.compute_distances(grid)
                print(render_distances(grid, a.distance_graph))
                actors.append(a)
    return actors


def render_distances(grid, distances):
    g = copy.deepcopy(grid)
    for p, d in distances.items():
        if d == INFINITY:
            d = "X"
        elif d > 9:
            d = "x"
        g.add(p, d)
    return g.render()

def nearest_enemy(actor, actors):
    pass


def solve1(grid):
    actors = extract_actors(grid, "EG")
    print(len(actors), " actors")
    actors.sort(key=lambda x: grid.linear_index(x.pos))

    for a in actors:
        print(a.symbol, a.pos)
        nearest_enemy(a, actors)


def run():
    # input_data = load_input_data(2018, 15)
    input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    grid = grid_from_lines(input_data)
    solve1(grid)
    # solve2(input_data)


if __name__ == "__main__":
    run()

import json
import math
from collections import defaultdict
from typing import Dict, Tuple, List

from aocd_tools import load_input_data, grid_from_lines, Grid
from dijkstra import Dijkstra, Step

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
        self.hit_points = 100
        self.distance_graph = defaultdict(lambda: math.inf)

    def serialise(self):
        return self.symbol, self.hit_points

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


def move_actor(move_from: Tuple, move_to: Tuple, actors: Dict[Tuple, Actor], grid: Grid):
    symbol = grid.at(move_from)
    grid.add(move_to, symbol)
    grid.add(move_from, ".")
    actors[move_to] = actors[move_from]
    actors[move_to].pos = move_to
    del (actors[move_from])


def extract_actors(grid, symbols="EG") -> Dict[Tuple, Actor]:
    actors = {}
    for y in range(grid.y_bounds.min, grid.y_bounds.max + 1):
        for x in range(grid.x_bounds.min, grid.x_bounds.max + 1):
            s = grid.at((x, y))
            if s in symbols:
                actors[(x, y)] = Actor((x, y), s)
    return actors


class EnemyFinder(Dijkstra):
    def __init__(self, initial_state, walls: Grid, actor: Actor):
        super().__init__(initial_state)
        self.walls = walls
        self.start = actor.pos
        self.enemy = "E" if actor.symbol = "G" else "G"

    @staticmethod
    def serialise(actors: Dict[Tuple, Actor]):
        goblins = {(v.pos.x, v.pos.y, v.hit_points) for k, v in actors.items() if v.symbol=="G"}
        elves = {(v.pos.x, v.pos.y, v.hit_points) for k, v in actors.items() if v.symbol=="E"}
        return sorted(goblins), sorted(elves)

    def valid_moves(self, actors: Dict[Tuple, Actor]) -> List[Step]:
        raise NotImplementedError

    @staticmethod
    def score(state) -> int:
        """Lower is better. 0 is winner"""
        return 0


def nearest_enemy(actor: Actor, actors: Dict[Tuple, Actor], grid: Grid):
    pass


def solve1(grid):
    actors = extract_actors(grid)
    print(len(actors), " actors")

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

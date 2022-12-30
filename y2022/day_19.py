import dataclasses
from dataclasses import astuple
import time
from dataclasses import dataclass
from functools import lru_cache
from math import prod
from typing import NamedTuple, List, Tuple, Optional

from aocd_tools import load_input_data# , get_elapsed

EXAMPLE = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian. 
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."""


def get_elapsed(t0: int):
    t = time.process_time()
    return t - t0

@dataclass
class Resources:
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0

    def add(self, right):
        self.ore += right.ore
        self.clay += right.clay
        self.obsidian += right.obsidian
        self.geode += right.geode

    def sub(self, right):
        self.ore -= right.ore
        self.clay -= right.clay
        self.obsidian -= right.obsidian
        self.geode -= right.geode

    def as_tuple(self):
        return (self.ore, self.clay, self.obsidian, self.geode)

class State(NamedTuple):
    robots: Resources
    resources: Resources
    time: int
    previous: Optional[Tuple]


def track_path(p: State):
    if not p:
        print("No solution found")
        return
    path = [p]
    while p.previous is not None:
        p = p.previous
        path.append(p)
    end_time = p.time
    print(f"Mining operation ran for {end_time} minutes")
    for p in reversed(path):
        print(f"Min{end_time - p.time:3}: ROBOTS {p.robots} | INVENTORY {p.resources}")


def best_possible(current_generators, time_left):
    return time_left * (current_generators + (1 + time_left) / 2)


class Blueprint(NamedTuple):
    id: int
    ore: Resources
    clay: Resources
    obsidian: Resources
    geode: Resources

    def most_ore_robots_needed(self):
        return max(self.ore.ore, self.clay.ore, self.obsidian.ore, self.geode.ore)

    def most_clay_robots_needed(self):
        return max(self.ore.clay, self.clay.clay, self.obsidian.clay, self.geode.clay)

    def geodes_mined(self, t):
        iterations = 0
        seen = set()
        initial_state = State(robots=Resources(ore=1),
                              resources=Resources(),
                              time=t, previous=None)
        queue = [initial_state]
        best = 0
        best_path = None
        while queue:
            iterations += 1
            if iterations % 10000 == 0:
                print(f"bp:{self.id} iter: {iterations} Q:{len(queue)} best:{best}")
            state = queue.pop()

            unique_state = (state.time, state.robots.as_tuple(), state.resources.as_tuple())
            if unique_state in seen:
                continue
            seen.add(unique_state)
            # collect resources
            resources = dataclasses.replace(state.resources)
            resources.add(state.robots)
            if state.resources.geode > best:
                best = state.resources.geode
                best_path = state
                print(f"bp:{self.id} iter: {iterations} Q:{len(queue)} best:{best}")

            if state.time == 0:
                continue
            if best_possible(state.robots.geode, state.time) + resources.geode <= best:
                continue
            # build robots
            prev = state
            queue.append(self.make_no_robots(resources, state.robots, state.time, prev))
            if can_build(self.ore, state.resources) and state.robots.ore < self.most_ore_robots_needed():
                queue.append(self.make_ore_robot(resources, state.robots, state.time, prev))
            if can_build(self.clay, state.resources) and state.robots.clay < self.most_clay_robots_needed():
                queue.append(self.make_clay_robot(resources, state.robots, state.time, prev))
            if can_build(self.obsidian, state.resources):
                queue.append(self.make_obsidian_robot(resources, state.robots, state.time, prev))
            if can_build(self.geode, state.resources):
                queue.append(self.make_geode_robot(resources, state.robots, state.time, prev))

        track_path(best_path)
        return best

    def make_no_robots(self, resources, robots, t, prev):
        res = dataclasses.replace(resources)
        rob = dataclasses.replace(robots)
        return State(resources=res, robots=rob, time=t - 1, previous=prev)

    def make_ore_robot(self, resources, robots, t, prev):
        res = dataclasses.replace(resources)
        res.sub(self.ore)
        rob = dataclasses.replace(robots)
        rob.ore += 1
        state = State(resources=res, robots=rob, time=t - 1, previous=prev)
        return state

    def make_clay_robot(self, resources, robots, t, prev):
        res = dataclasses.replace(resources)
        res.sub(self.clay)
        rob = dataclasses.replace(robots)
        rob.clay += 1
        return State(resources=res, robots=rob, time=t - 1, previous=prev)

    def make_obsidian_robot(self, resources, robots, t, prev):
        res = dataclasses.replace(resources)
        res.sub(self.obsidian)
        rob = dataclasses.replace(robots)
        rob.obsidian += 1
        return State(resources=res, robots=rob, time=t - 1, previous=prev)

    def make_geode_robot(self, resources, robots, t, prev):
        res = dataclasses.replace(resources)
        res.sub(self.geode)
        rob = dataclasses.replace(robots)
        rob.geode += 1
        return State(resources=res, robots=rob, time=t - 1, previous=prev)


def can_build(needed, got):
    if needed.ore > got.ore:
        return False
    if needed.clay > got.clay:
        return False
    if needed.obsidian > got.obsidian:
        return False
    return True


def make_blueprint(entry):
    lines = entry.split("Each ")
    id_num = int(lines[0].split()[-1][:-1])
    ore = int(lines[1].split()[3])
    clay = int(lines[2].split()[3])
    obsidian = int(lines[3].split()[3]), int(lines[3].split()[6])
    geode = int(lines[4].split()[3]), int(lines[4].split()[6])
    return Blueprint(id_num,
                     ore=Resources(ore=ore),
                     clay=Resources(ore=clay),
                     obsidian=Resources(ore=obsidian[0], clay=obsidian[1]),
                     geode=Resources(ore=geode[0], obsidian=geode[1])
                     )


def run():
    input_data = load_input_data(2022, 19)
    # input_data = EXAMPLE

    print(f"loaded input data ({len(input_data)} bytes)")

    entries = input_data.split("\n")
    entries = [make_blueprint(line) for line in entries]
    print(entries[:50])

    t = time.process_time()
    #print("solution1 = ", solution1(entries))
    dt = get_elapsed(t)
    print(f"in {dt}")
    t = time.process_time()
    print("solution2 = ", solution2(entries))
    dt = get_elapsed(t)
    print(f"in {dt}")


def solution1(blueprints):
    geodes = {blueprint.id: blueprint.geodes_mined(24) for blueprint in blueprints}
    quality_levels = [i * v for i, v in geodes.items()]
    return sum(quality_levels)


def solution2(blueprints):
    geodes = {blueprint.id: blueprint.geodes_mined(32) for blueprint in blueprints[:3]}
    return prod(geodes.values())


if __name__ == "__main__":
    run()

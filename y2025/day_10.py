from typing import NamedTuple

import dijkstra
from aocd_tools import Grid
from y2025.day10_data import DATA

EXAMPLE = """
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
""".strip()


class Machine(NamedTuple):
    lights: int
    buttons: int
    joltage_req: tuple[int, ...]

def parse(data):
    lines = [line.strip() for line in data.strip().split("\n")]
    machines = []
    for line in lines:
        parts = line.split()
        lights = make_lights(parts[0][1:-1])
        joltage_req = tuple(int(x) for x in parts[-1][1:-1].split(","))
        buttons = [make_buttons(x) for x in parts[1:-1]]
        machine = Machine(lights, buttons, joltage_req)
        machines.append(machine)
    return machines


def make_lights(s):
    s = s[::-1]
    s = s.replace("#", "1")
    s= s.replace(".", "0")
    return eval(f"0b{s}")

def make_buttons(s):
    b = eval(s)
    if isinstance(b, int):
        b = (b,)
    result = 0
    for but in b:
        result |= 1 << but
    return result


class LightsSolver(dijkstra.Dijkstra):
    def __init__(self, buttons, destination: int) -> None:
        self.destination = destination
        super().__init__(initial_state=0)
        self.state = 0
        self.buttons = buttons

    def is_win(self, state) -> bool:
        return state == self.destination

    def valid_moves(self, state) -> list[dijkstra.Step]:
        moves = []
        for button in self.buttons:
            cost = 1
            new_state = self.state ^ button
            print(f"{state} + {button} -> {new_state}")
            moves.append(dijkstra.Step(cost=cost, state=new_state))
        return moves

    def report(self) -> None:
        print(self.visited, "\n", self.nodes)

def part1():
    machines = parse(EXAMPLE)
    results = []
    for machine in machines:
        solver = LightsSolver(machine.buttons, destination=machine.lights)
        best_cost = solver.search()
        results.append(best_cost)
    return sum(results)


def part2():
    result = 0
    return result


if __name__ == "__main__":
    print("part1:", part1())
    print("part2:", part2())

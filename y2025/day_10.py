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
    buttons: tuple[int, ...]
    button_sets: tuple[set[int]]
    joltage_req: tuple[int, ...]

def parse(data):
    lines = [line.strip() for line in data.strip().split("\n")]
    machines = []
    for line in lines:
        parts = line.split()
        lights = make_lights(parts[0][1:-1])
        joltage_req = tuple(int(x) for x in parts[-1][1:-1].split(","))
        buttons = tuple(make_buttons(x) for x in parts[1:-1])
        button_sets = tuple(make_buttons_set(x) for x in parts[1:-1])
        machine = Machine(lights, buttons, button_sets, joltage_req)
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


def make_buttons_set(s):
    b = eval(s)
    if isinstance(b, int):
        b = (b,)
    return set(b)


class LightsSolver(dijkstra.Dijkstra):
    def __init__(self, buttons, destination: int) -> None:
        self.destination = destination
        super().__init__(initial_state=0)
        self.buttons = buttons

    def is_win(self, state) -> bool:
        return state == self.destination

    def valid_moves(self, state) -> list[dijkstra.Step]:
        moves = []
        for button in self.buttons:
            cost = 1
            new_state = state ^ button
            # print(f"{state} + {button} -> {new_state}")
            moves.append(dijkstra.Step(cost=cost, state=new_state))
        return moves

    # def report(self) -> None:
    #     print(self.visited, "\n", self.nodes)

def part1():
    machines = parse(DATA)
    results = []
    for machine in machines:
        solver = LightsSolver(machine.buttons, destination=machine.lights)
        best_cost = solver.search()
        results.append(best_cost)
    return sum(results)


class JoltSolver(dijkstra.Dijkstra):
    def __init__(self, buttons, destination: tuple[int, ...], initial_joltage) -> None:
        self.destination = destination
        super().__init__(initial_state=initial_joltage)
        self.buttons = buttons

    def is_win(self, state) -> bool:
        return state == self.destination

    def valid_moves(self, state) -> list[dijkstra.Step]:
        moves = []
        for button in self.buttons:
            cost = 1
            new_state = tuple(x + int(i in button) for i, x in enumerate(state))
            if any(a < b for a, b in zip(self.destination, new_state)):
                continue
            # print(f"{state} + {button} -> {new_state}")
            moves.append(dijkstra.Step(cost=cost, state=new_state))
        return moves


def part2():
    machines = parse(DATA)
    results = []
    for machine in machines:
        joltage, buttons, pre_count = trim(machine)
        solver = JoltSolver(buttons, destination=machine.joltage_req, initial_joltage=tuple(joltage))
        best_cost = solver.search()
        # path = solver.get_best_path(tuple(joltage), machine.joltage_req)
        # print(path)
        print(best_cost)
        results.append(best_cost + pre_count)
    return sum(results)

def trim(machine: Machine):
    joltage = [0] * len(machine.joltage_req)
    buttons = list(machine.button_sets)
    moves = 0
    print(buttons)
    finished = False
    while not finished:
        for i, button in enumerate(buttons):
            unique = button.copy()
            for j, sub_b in enumerate(buttons):
                if j == i:
                    continue
                unique -= sub_b
            if unique:
                for n in unique:  # probably only one but just get one
                    break
                presses = machine.joltage_req[n] - joltage[n]
                moves += presses
                for n in button:
                    joltage[n] += presses
                del buttons[i]
                break
        else:
            finished = True
    return joltage, buttons, moves


if __name__ == "__main__":
    # print("part1:", part1())
    print("part2:", part2())

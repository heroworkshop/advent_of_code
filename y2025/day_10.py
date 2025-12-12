from contextlib import suppress
from pprint import pprint
from typing import NamedTuple

import numpy as np

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
    machines = parse(EXAMPLE)
    results = []
    for machine in machines:
        results.append(solve_with_gausian_elimination(machine))
        # joltage, buttons, pre_count = trim(machine)
        # solver = JoltSolver(buttons, destination=machine.joltage_req, initial_joltage=tuple(joltage))
        # best_cost = solver.search()
        # # path = solver.get_best_path(tuple(joltage), machine.joltage_req)
        # # print(path)
        # print(best_cost)
        # results.append(best_cost + pre_count)
    return sum(results)


def solve_with_gausian_elimination(machine: Machine):
    rows = [
        [
            int(n in button) for button in machine.button_sets
        ]
        for n, _ in enumerate(machine.joltage_req)
    ]

    for row, joltage in zip(rows, machine.joltage_req):
        row.append(joltage)
    pprint(rows)
    print("-" * 30)
    for target_row, _ in enumerate(rows):
        target_col = target_row
        if target_col > len(rows[0]) - 1:
            break
        print(f"Get a 1 in the r{target_row} c{target_col} by swapping")
        if rows[target_row][target_col] == -1:
            divide_row(rows[target_row], -1)
        with suppress(IndexError):
            if rows[target_row][target_col] == 0:
                i = find_non_zero(rows, target_row + 1, target_col)
                swap_rows(rows, target_row, i)
        pprint(rows)
        print(f"eliminate non-zeros in col{target_col} using row{target_row}")
        for row in rows[target_row + 1:]:
            if row[target_col] != 0:
                m = row[target_col]
                subtract(row, rows[target_row], m)
        pprint(rows)

    print("eliminate free rows")
    mark = []
    for i, row in enumerate(rows):
        if all(x==0 for x in row):
            mark.append(i)

    for m in mark[::-1]:
        del rows[m]

    pprint(rows)

    print("Now go the other way")
    target_col = -1
    for i, _ in enumerate(rows):
        target_row = -i - 1
        target_col -= 1
        print(f"eliminate non-zeros in col{target_col} using row{target_row}")
        for row in rows[:target_row]:
            if row[target_col] != 0:
                m = row[target_col]
                subtract(row, rows[target_row], m)
        pprint(rows)
    result = sum(row[-1] for row in rows)
    print("button presses = ", result)
    return result

def subtract(row_from, row_by, multiplier: int):
    for i, v in enumerate(row_by):
        row_from[i] -= v * multiplier


def find_non_zero(rows, r, c):
    while rows[r][c] == 0:
        r += 1
    divide_row(rows[r], rows[r][c])
    return r

def divide_row(row, d):
    for i, v in enumerate(row):
        row[i] = v // d

def swap_rows(rows, r1, r2):
    rows[r1], rows[r2] = rows[r2], rows[r1]


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

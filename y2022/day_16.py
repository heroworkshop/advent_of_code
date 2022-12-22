import math
from collections import defaultdict
from typing import Dict, List, NamedTuple, Tuple

from aocd_tools import load_input_data
from y2022.dual_valve_solver import DualValveSolver, DualState
from y2022.valve_solver import ValveSolver, Node, State

EXAMPLE = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""

EX2 = """Valve AA has flow rate=0; tunnels lead to valves DD, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA"""


def run():
    input_data = load_input_data(2022, 16)
    # input_data = EXAMPLE

    print(f"loaded input data ({len(input_data)} bytes)")

    entries = input_data.split("\n")
    node_list = [parse(line) for line in entries]
    print(node_list[:50])

    nodes = make_nodes(node_list)

    paths = shortest_path_table(nodes)

    print("Solution 1 = ", solution1(nodes, paths))
    print("solution2 = ", solution2(nodes, paths))  # > 2248


class Trip(NamedTuple):
    node_name: str
    time: int
    energy: int
    rates: Dict[str, int]


def solution1(nodes, paths):
    best = 0
    stack = [Trip("AA", 30, 0, {name: node.rate for name, node in nodes.items()})]
    while stack:
        cur_trip = stack.pop(-1)

        values = reversed(sorted([((cur_trip.time - cost) * cur_trip.rates[name], name)
                                  for name, cost in paths[cur_trip.node_name].items()
                                  if cur_trip.rates[name]]))
        if not values:
            continue
        for _, next_node in values:
            cost = paths[cur_trip.node_name][next_node]
            time = cur_trip.time - (cost + 1)  # cost to get there plus 1 to open valve
            if time <= 0:
                continue
            energy = cur_trip.energy + cur_trip.rates[next_node] * time
            if energy > best:
                best = energy
                print("Energy: ", energy)
            rates = cur_trip.rates.copy()
            rates[next_node] = 0
            stack.append(Trip(next_node, time, energy, rates))
    return best


class DualTrip(NamedTuple):
    node_name: Tuple[str, str]
    time: Tuple[int, int]
    energy: int
    rates: Dict[str, int]


def solution2(nodes, paths):
    iterations = 0
    pruned = 0
    best = 0
    stack = [DualTrip(("AA", "AA"), (26, 26), 0, {name: node.rate for name, node in nodes.items()})]
    while stack:
        cur_trip = stack.pop(-1)
        iterations += 1
        if iterations % 100000 == 0:
            print(f"{iterations} Q={len(stack)}")
        player = 1 if cur_trip.time[1] > cur_trip.time[0] else 0
        node_name = cur_trip.node_name[player]
        values = reversed(sorted([((cur_trip.time[player] - cost) * cur_trip.rates[name], name)
                         for name, cost in paths[node_name].items()
                         if cur_trip.rates[name]]))
        if not values:
            continue
        for _, next_node in values:
            cost = paths[cur_trip.node_name[player]][next_node]
            time = cur_trip.time[player] - (cost + 1)  # cost to get there plus 1 to open valve
            if time <= 0:
                continue
            energy = cur_trip.energy + cur_trip.rates[next_node] * time
            if energy > best:
                best = energy
                print("Energy: ", energy)
            rates = cur_trip.rates.copy()
            rates[next_node] = 0
            node_names = list(cur_trip.node_name)
            node_names[player] = next_node
            new_times = list(cur_trip.time)
            new_times[player] = time
            stack.append(DualTrip(tuple(node_names), tuple(new_times), energy, rates))
    return best


def parse(line: str):
    parts = line.split()
    name = parts[1]
    _, _, rate = parts[4].partition("=")
    exits = [p.replace(",", "") for p in parts[9:]]
    return Node(name=name, rate=int(rate[:-1]), exits=exits)


def make_nodes(node_list) -> Dict[str, Node]:
    return {node.name: node for node in node_list}


#
# def solution2(nodes):
#     solver = solve_dual(nodes, 26)
#
#     for p in solver.best_path:
#         print(p)
#
#     return solver.best
#
#
# def solve_dual(nodes, start_time):
#     rates = {name: node.rate for name, node in nodes.items()}
#     initial_state = DualState(cur_node="AA", ele_node="AA", rates=rates, score=0, time=start_time)
#     solver = DualValveSolver(initial_state=initial_state, nodes=nodes)
#     solver.search()
#     return solver

def shortest_path_table(nodes: Dict[str, Node]):
    table = {name: defaultdict(lambda: math.inf) for name in nodes}
    for from_node in nodes:
        stack = [(from_node, 0)]
        while stack:
            name, cost = stack.pop()
            if table[from_node][name] < cost:
                cost = table[from_node][name]
            else:
                for next_node in nodes[name].exits:
                    stack.append((next_node, cost + 1))
            table[from_node][name] = cost
            table[name][from_node] = cost
    show_table(table, nodes.keys())
    return table


def show_table(table, names):
    print("\n      ", end="")
    for n in names:
        print(f"{n:4}", end="")
    print()
    for name, row in table.items():
        print(name, " ", end="")
        for n in names:
            print(f"{row[n]:4}", end="")
        print()


if __name__ == "__main__":
    run()

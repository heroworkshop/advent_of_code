# The first floor contains a promethium generator and a promethium-compatible microchip.
# The second floor contains a cobalt generator, a curium generator, a ruthenium generator, and a plutonium generator.
# The third floor contains a cobalt-compatible microchip, a curium-compatible microchip, a ruthenium-compatible microchip, and a plutonium-compatible microchip.
# The fourth floor contains nothing relevant.
from copy import deepcopy
from itertools import combinations
from typing import NamedTuple, Set, List

from dijkstra import Dijkstra, Step


class State(NamedTuple):
    elevator: int
    floors: List[Set]


FLOORS = State(elevator=3, floors=[set(),
                                   {"CoM", "CuM", "RuM", "PuM"},
                                   {"CoG", "CuG", "RuG", "PuG"},
                                   {"PrG", "PrM"},
                                   ])

FLOORS_2 = State(elevator=3, floors=[set(),
                                   {"CoM", "CuM", "RuM", "PuM"},
                                   {"CoG", "CuG", "RuG", "PuG"},
                                   {"PrG", "PrM", "EG", "EM", "DG", "DM"},
                                   ])

FLOORS_ = State(elevator=3, floors=[set(),
                                    {"LiG"},
                                    {"HeG"},
                                    {"HeM", "LiM"},
                                    ],
                )


class ElevatorSolver(Dijkstra):
    @staticmethod
    def serialise(state: State):
        return f"{state.elevator}" + \
               "\n".join([" ".join(sorted(floor)) for floor in state.floors])

    @staticmethod
    def score(state: State) -> int:
        """Lower is better. 0 is winner"""
        s = sum(floor * len(names) for floor, names in enumerate(state.floors))
        return int(bool(s))

    def valid_moves(self, state: State) -> List[Step]:
        moves: List[Step] = []
        destinations = [n for n in (state.elevator + 1, state.elevator - 1) if n in range(len(state.floors))]
        for destination in destinations:
            pairs = set(combinations(state.floors[state.elevator], 2))
            singles = {(i, i) for i in state.floors[state.elevator]}
            for item1, item2 in pairs.union(singles):
                new_state = State(destination, deepcopy(state.floors))
                new_state.floors[state.elevator].difference_update({item1, item2})
                new_state.floors[destination].update({item1, item2})
                if self.is_valid(new_state.floors):
                    moves.append(Step(1, new_state))

        return moves

    def is_valid(self, floors: List[Set]) -> bool:
        for floor in floors:
            generators = set()
            microchips = set()
            for item in floor:
                flavour = self.item_flavour(item)
                if self.is_microchip(item):
                    microchips.add(flavour)
                if self.is_generator(item):
                    generators.add(flavour)
            for chip in microchips:
                if chip not in generators and generators.difference({chip}):
                    return False
        return True

    @staticmethod
    def is_generator(name):
        return name.endswith("G")

    @staticmethod
    def is_microchip(name):
        return name.endswith("M")

    @staticmethod
    def item_flavour(name):
        return name[:-1]


def main():
    solver = ElevatorSolver(FLOORS_2)
    result = solver.search()
    print(result)


if __name__ == "__main__":
    main()

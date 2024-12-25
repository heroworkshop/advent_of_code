import heapq
import math
import time
from typing import List, NamedTuple, Any


class Step(NamedTuple):
    cost: int
    state: Any

class Node(NamedTuple):
    cost: int
    from_state: list[Any]


class Dijkstra:
    def __init__(self, initial_state):
        self.visited = set()
        self.nodes: dict[Any: Node] = {}
        self.queue = []
        self.iterations = 0
        self.report_rate = 10000  # print progress after this many iterations
        self.add_move(0, initial_state)
        self.start_time = 0
        self.end_time = 0

        self.best = math.inf
        self.single_solution = True

    @property
    def time_taken(self):
        return self.end_time - self.start_time

    def add_move(self, step_count: int, state: Any):
        heapq.heappush(self.queue, Step(step_count, state=state))

    @staticmethod
    def serialise(state):
        return state

    def is_win(self, state) -> bool:
        raise NotImplementedError

    def valid_moves(self, state) -> List[Step]:
        raise NotImplementedError

    def search(self):
        """Will find best path. Returns math.inf if no path exists"""
        self.start_time = time.process_time()
        while self.queue:
            move: Step = heapq.heappop(self.queue)
            self.iterations += 1
            if self.is_win(move.state):
                self.best = move.cost
                if self.single_solution:
                    return move.cost
            if move.state in self.visited:
                continue
            self.queue_new_moves(move, move.state)
            self.report()
            self.visited.add(move.state)

        self.end_time = time.process_time()
        return self.best

    def report(self):
        if self.iterations % self.report_rate:
            return
        print(f"{self.iterations:6} Q:{len(self.queue):6}")

    def get_best_path(self, to_node, from_node):
        path = [to_node]
        node = to_node
        while node != from_node:
            node = self.nodes[node].from_state[0]
            path.append(node)
        return path[::-1]

    def get_all_best_path_states(self, to_node, from_node):
        states = set()
        queue = [to_node]
        while queue:
            state = queue.pop(0)
            states.add(state)
            if state == from_node:
                break
            for node in self.nodes[state].from_state:
                queue.append(node)
        return states


    def queue_new_moves(self, move: Step, from_state: Any):
        for cost, new_move_state in self.valid_moves(move.state):
            new_cost = move.cost + cost
            s = self.serialise(new_move_state)
            if s not in self.nodes or self.nodes[s].cost > new_cost:
                self.nodes[s] = Node(new_cost, [from_state])
            elif self.nodes[s].cost == new_cost:
                self.nodes[s].from_state.append(from_state)
            self.add_move(self.nodes[s].cost, new_move_state)

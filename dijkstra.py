import heapq
import time
from typing import List, NamedTuple, Any


class Move(NamedTuple):
    step_count: int
    state: Any
    path: List[Any]


class Step(NamedTuple):
    cost: int
    state: Any


class Dijkstra:
    def __init__(self, initial_state):
        self.visited = set()
        self.queue = []
        self.best = float("inf")
        self.best_path = None
        self.pruned = 0  # removed because a shorter path has been found already
        self.duplicates = 0  # path ignored because node has already been visited
        self.iterations = 0
        self.report_rate = 1000  # print progress after this many iterations
        self.store_path = False
        self.add_move(0, initial_state, [])
        self.start_time = 0
        self.end_time = 0

    @property
    def time_taken(self):
        return self.end_time - self.start_time

    def add_move(self, step_count: int, state: Any, current_path: List):
        self.visited.add(self.serialise(state))
        path = []
        if self.store_path:
            path = current_path[:]
            path.append(state)
        heapq.heappush(self.queue, Move(step_count=step_count,  state=state, path=path))

    @staticmethod
    def serialise(state):
        raise NotImplementedError

    @staticmethod
    def is_win(self, state) -> bool:
        raise NotImplementedError

    def valid_moves(self, state) -> List[Step]:
        raise NotImplementedError

    def search(self):
        self.start_time = time.process_time()
        while self.queue:
            move: Move = heapq.heappop(self.queue)
            self.iterations += 1

            if self.is_win(move.state):
                return move.step_count
            self.queue_new_moves(move)
            self.report()

        self.end_time = time.process_time()
        return self.best

    def report(self):
        if self.iterations % self.report_rate:
            return
        print(f"{self.iterations:6} Q:{len(self.queue):6} Prune:{self.pruned:6} Dups:{self.duplicates:6} Best:{self.best}")

    def queue_new_moves(self, move):
        for cost, new_move_state in self.valid_moves(move.state):
            new_step_count = move.step_count + cost
            if self.serialise(new_move_state) in self.visited:
                self.duplicates += 1
                continue
            self.add_move(new_step_count, new_move_state, move.path)

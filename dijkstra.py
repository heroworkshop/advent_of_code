import heapq
from typing import List, NamedTuple, Any


class Move(NamedTuple):
    score: int
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

    def add_move(self, step_count: int, state: Any, current_path: List):
        self.visited.add(self.serialise(state))
        path = current_path[:]
        if self.store_path:
            path.append(state)
        heapq.heappush(self.queue, Move(step_count=step_count, score=self.score(state), state=state, path=path))

    @staticmethod
    def serialise(state):
        raise NotImplementedError

    @staticmethod
    def score(state) -> int:
        """Lower is better. 0 is winner"""
        return 0

    def valid_moves(self, state) -> List[Step]:
        raise NotImplementedError

    def search(self):
        while self.queue:
            move: Move = heapq.heappop(self.queue)
            self.iterations += 1

            if move.score == 0:
                self.best = min(self.best, move.step_count)
                self.best_path = move.path
                continue
            self.queue_new_moves(move)
            self.report()

        return self.best

    def report(self):
        if self.iterations % self.report_rate:
            return
        print(f"{self.iterations:6} Q:{len(self.queue):6} Prune:{self.pruned:6} Dups:{self.duplicates:6}")

    def queue_new_moves(self, move):
        for cost, new_move_state in self.valid_moves(move.state):
            new_step_count = move.step_count + cost
            if self.serialise(new_move_state) in self.visited:
                self.duplicates += 1
                continue
            if new_step_count >= self.best:
                self.pruned += 1
                continue
            self.add_move(new_step_count, new_move_state, move.path)

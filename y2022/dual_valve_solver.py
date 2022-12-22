import heapq
import json
import time
from typing import List, NamedTuple, Dict

from dijkstra import Dijkstra, Step


class DualState(NamedTuple):
    cur_node: str
    ele_node: str
    rates: Dict[str, int]
    time: int
    score: int

    def __lt__(self, other):
        return False


class Move(NamedTuple):
    score: int
    state: DualState
    path: List[DualState]
    step_count: int


class DualValveSolver(Dijkstra):
    def __init__(self, initial_state, nodes):
        self.nodes = nodes
        super().__init__(initial_state)
        self.store_path = True
        self.best = 0

    def add_move(self, step_count: int, state: DualState, current_path: List):
        self.visited.add(self.serialise(state))
        path = []
        if self.store_path:
            path = current_path[:]
            path.append(state)
        heapq.heappush(self.queue, Move(score=-state.score, step_count=step_count, state=state, path=path))

    @staticmethod
    def serialise(state):
        return (state.cur_node, state.ele_node, state.score, tuple([state.rates[k] for k in sorted(state.rates)]))
        # return json.dumps(
        #     {"cur_node": state.cur_node, "ele_node": state.ele_node, "rates": state.rates, "score": state.score})

    def score(self, state) -> int:
        """Lower is better"""
        return -state.score

    def valid_moves(self, state: DualState) -> List[Step]:
        moves = []
        t = state.time - 1
        if not any(state.rates.values()):
            return moves

        # Open Valve
        if state.rates[state.cur_node]:
            new_rates = state.rates.copy()
            score = state.rates[state.cur_node] * t + state.score
            new_rates[state.cur_node] = 0
            # you open valve but elephant moves
            for ele_dest in self.nodes[state.ele_node].exits:
                moves.append(Step(1, DualState(cur_node=state.cur_node, ele_node=ele_dest, rates=new_rates, score=score,
                                               time=t)))

            # Both open valve
            if new_rates[state.ele_node]:
                new_rates = new_rates.copy()
                score += new_rates[state.ele_node] * t
                new_rates[state.ele_node] = 0
                moves.append(
                    Step(1, DualState(cur_node=state.cur_node, ele_node=state.ele_node, rates=new_rates, score=score,
                                      time=t)))
        # move to a different location
        for dest in self.nodes[state.cur_node].exits:
            if state.rates[state.ele_node] and state.ele_node != state.cur_node:
                # elephant opens valve
                new_rates = state.rates.copy()
                score = state.rates[state.ele_node] * t + state.score
                new_rates[state.ele_node] = 0
                moves.append(Step(1, DualState(cur_node=dest, ele_node=state.ele_node, rates=new_rates, score=score,
                                               time=t)))
            for ele_dest in self.nodes[state.ele_node].exits:
                # if state.cur_node == state.ele_node and ele_dest == dest:
                #     continue
                new_state = DualState(cur_node=dest, ele_node=ele_dest, rates=state.rates, score=state.score,
                                      time=t)
                moves.append(Step(cost=1, state=new_state))
        return moves

    def queue_new_moves(self, move):
        for cost, new_move_state in self.valid_moves(move.state):

            new_step_count = move.step_count + cost
            serialised = self.serialise(new_move_state)
            if serialised in self.visited:
                # print(f"already visited {serialised}")
                self.duplicates += 1
                continue
            if not new_move_state.time:
                self.pruned += 1
                continue
            self.add_move(new_step_count, new_move_state, move.path)

    def search(self):
        self.start_time = time.process_time()
        while self.queue:
            move: Move = heapq.heappop(self.queue)
            # print(move)
            self.iterations += 1

            if move.state.score > self.best:
                self.best = move.state.score
                self.best_path = move.path
            self.queue_new_moves(move)
            self.report()

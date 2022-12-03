import heapq
from collections import namedtuple
from copy import deepcopy
from itertools import count, zip_longest

HALLWAY_LENGTH = 7
ROOM_DEPTH = 4

Move = namedtuple("move", "score energy board")

"""
###B#C#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########"""
EXAMPLE = "ADDB", "DBCC", "CABB", "ACAD"
"""
#############
#...........#
###B#B#C#D###
  #D#C#B#A#
  #D#B#A#C#
  #D#A#A#C#
  #########"""

INPUT_DATA = "DDDB", "ABCB", "AABC", "CCAD"

AMPHIPOD_TYPES = {
    "A": (1, 0),
    "B": (10, 1),
    "C": (100, 2),
    "D": (1000, 3),
}

HOME_CHARS = {
    v[1]: ch for ch, v in AMPHIPOD_TYPES.items()
}


class Amphipod:
    def __init__(self, type_ch):
        self.type = type_ch
        self.energy, self.home = AMPHIPOD_TYPES[type_ch]

    def is_home(self, room, room_number):
        if self.home != room_number:
            return False
        if any(a != self.type for a in room.slots):
            return False
        return True


class RoomFull(ValueError):
    pass


class RoomEmpty(IndexError):
    pass


class Room:
    def __init__(self, occupants=""):
        self.slots = list(occupants) if occupants else []

    @property
    def depth(self):
        return ROOM_DEPTH - len(self.slots)

    def empty(self):
        return self.depth == ROOM_DEPTH

    def push(self, ch):
        if len(self.slots) == ROOM_DEPTH:
            raise RoomFull
        self.slots.append(ch)

    def pop(self):
        if not self.slots:
            raise RoomEmpty
        return self.slots.pop(-1)

    def __hash__(self):
        return "".join(self.slots)

    def __str__(self):
        s = "".join(reversed(self.slots))
        return s.rjust(ROOM_DEPTH, ".")


"""
#############
#01.2.3.4.56#
###0#1#2#3###
"""
DISTANCES = {
    0: [3, 2, 2, 4, 6, 8, 9],
    1: [5, 4, 2, 2, 4, 6, 7],
    2: [7, 6, 4, 2, 2, 4, 5],
    3: [9, 8, 6, 4, 2, 2, 3],
}

PATHS = {
    0: (1, 2),
    1: (2, 3),
    2: (3, 4),
    3: (4, 5),
}


def distance(hall_id, room_id, depth):
    return DISTANCES[room_id][hall_id] + depth


class GameBoard:
    def __init__(self, rooms=tuple(), hallway=""):
        positions = {0: 0, 1: 1, 3: 2, 5: 3, 7: 4, 9: 5, 10: 6}
        self.hallway = {positions[k]: v for k, v in enumerate(hallway) if v != "."}
        self.rooms = [Room(r) for r, _ in zip_longest(rooms, range(4))]
        self.piece_count = len(self.hallway) + sum(len(r.slots) for r in self.rooms)
        self.parent = None
        self.energy = 0

    def as_tuple(self):
        h = tuple(self.hallway.items())
        r = tuple(r.__hash__() for r in self.rooms)
        return h, r

    def __hash__(self):
        return self.as_tuple().__hash__()

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __lt__(self, other):
        return self.as_tuple() < other.as_tuple()

    def __str__(self):
        hallway = "#01.2.3.4.56#"
        for i in range(HALLWAY_LENGTH):
            hallway = hallway.replace(str(i), self.hallway.get(i, "."))
        rooms = "\n".join(
            f"###{a}#{b}#{c}#{d}###"
            for a, b, c, d in zip(*[str(r) for r in self.rooms])
        )

        return (f"#############\n"
                f"{hallway}\n"
                f"{rooms}")

    def moves(self, base_energy):
        hallway_moves = self.room_to_hallway_moves(base_energy)
        room_moves = self.hallway_to_room_moves(base_energy)
        return [*hallway_moves, *room_moves]

    def hallway_to_room_moves(self, base_energy):
        moves = []
        for hall_id, ch in self.hallway.items():
            amphipod = Amphipod(ch)
            room_id = amphipod.home
            room = self.rooms[room_id]
            if amphipod.is_home(room, room_id) and self.path_clear(hall_id, room_id):
                new_board = deepcopy(self)
                new_board.parent = self
                new_board.hallway.pop(hall_id)
                new_board.rooms[room_id].push(ch)
                new_board.energy = base_energy + amphipod.energy * distance(hall_id, room_id, room.depth - 1)
                score = new_board.count_winners()
                moves.append(Move(-score, new_board.energy, new_board))
        return moves

    def room_to_hallway_moves(self, base_energy):
        moves = []
        for room_number, _ in enumerate(self.rooms):
            room = self.rooms[room_number]
            if room.empty():
                continue
            depth = room.depth
            board_template = deepcopy(self)
            ch = board_template.rooms[room_number].pop()
            amphipod = Amphipod(ch)
            if amphipod.is_home(room, room_number):
                continue
            # shortcut hallway
            # if amphipod.is_home(self.rooms[amphipod.home], amphipod.home) and self.path_clear_room_to_room(amphipod.home, room_number):
            #     new_board = deepcopy(self)
            #     new_board.parent = self
            #     new_board.rooms[amphipod.home].push(ch)
            #     new_board.energy = base_energy + amphipod.energy * distance(hall_id, room_id, room.depth - 1)
            #     score = new_board.count_winners()
            #     moves.append(Move(-score, new_board.energy, new_board))
            #     break
            for hall_id in range(HALLWAY_LENGTH):
                if hall_id not in board_template.hallway and self.path_clear(hall_id, room_number):
                    new_board = deepcopy(board_template)
                    new_board.parent = self
                    new_board.hallway[hall_id] = ch
                    new_board.energy = base_energy + amphipod.energy * distance(hall_id, room_number, depth)
                    score = new_board.count_winners()
                    moves.append(Move(-score, new_board.energy, new_board))
        return moves

    def path_clear(self, hall_id, room_id):
        path_left, path_right = PATHS[room_id]
        path = range(hall_id + 1, path_left + 1) if hall_id <= path_left else range(path_right, hall_id)
        return not any(p in self.hallway and p != hall_id for p in path)

    def count_winners(self):
        count = 0
        for room_id, room in enumerate(self.rooms):
            home_ch = HOME_CHARS[room_id]
            for ch in room.slots:
                if ch == home_ch:
                    count += 1
        return count

    def is_winner(self):
        return self.count_winners() == self.piece_count


def run(rooms):
    g0 = GameBoard(rooms=rooms)
    queue = []
    visited = {}
    heapq.heappush(queue, Move(0, 0, g0))
    best_winner = 1000000
    n = 0
    while queue:
        n += 1
        score, energy, gameboard = heapq.heappop(queue)
        if n % 10000 == 0:
            print(f"{n} score: {-score} queue:{len(queue)}")
        if energy >= best_winner:
            continue
        moves: Move = gameboard.moves(energy)
        for move in moves:
            # print(f"{move.board}\n{move.energy}")
            if move.board.is_winner() and move.energy < best_winner:
                print(f"NEW WINNER:\n{move.board}\n{move.energy}")
                best_winner = move.energy
                record_win(move.board)
            if move.board in visited and visited[move.board] <= move.energy:
                continue
            visited[move.board] = move.energy
            heapq.heappush(queue, move)
    print("Solution:", best_winner)
    return best_winner


def record_win(board):
    with open(f"{board.energy}.txt", "w") as f:
        while True:
            print(f"{board}\n{board.energy}\n", file=f)
            if not board.parent:
                break
            board = board.parent


if __name__ == "__main__":
    run(INPUT_DATA)

import heapq
from collections import defaultdict, namedtuple

from aocd_tools import load_input_data
from itertools import count

EXAMPLE = """
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
"""

"""
#############
#01.2.3.4.56#
###3#7#b#f###
  #2#6#a#e#
  #1#5#9#d#
  #0#4#8#c#
  #########
"""

PATHS = {
    4: (1, 2),
    8: (2, 3),
    12: (3, 4),
    16: (4, 5)
}

"""
  0 1 2 3 4 5 6 
0 6 5 5 7 9 B C
1 5 4 4 6 8 A B
2 4 3 3 5 7 9 A
3 3 2 2 4 6 8 B
4 8 7 5 5 7 9 A 
5 7 6 4 4 6 8 9
6 6 5 3 3 5 7 8
7 5 4 2 2 4 6 7
8 A 9 7 5 5 7 8
9 9 8 6 4 4 6 7
A 8 7 5 3 3 5 6
B 7 6 4 2 2 4 5
C C B 9 7 5 5 6
D B A 8 6 4 4 5
E A 9 7 5 3 3 4
F 9 8 6 4 2 2 3
"""

DISTANCES = """
6 5 5 7 9 B C
5 4 4 6 8 A B
4 3 3 5 7 9 A
3 2 2 4 6 8 B
8 7 5 5 7 9 A 
7 6 4 4 6 8 9
6 5 3 3 5 7 8
5 4 2 2 4 6 7
A 9 7 5 5 7 8
9 8 6 4 4 6 7
8 7 5 3 3 5 6
7 6 4 2 2 4 5
C B 9 7 5 5 6
B A 8 6 4 4 5
A 9 7 5 3 3 4
9 8 6 4 2 2 3
""".strip()

seqnum = count()

distances = [
    [int(v, 16) for v in line.split()]
    for line in DISTANCES.split("\n")
]

HALLWAY_COUNT = 7
ROOM_COUNT = 16
Amphipod = namedtuple("amphipod", "start_pos energy rooms type")

Move = namedtuple("move", "score energy seqnum board")


def distance(room, hallway):
    return distances[room][hallway]


def cost(amphipod, room, hallway):
    return distance(room, hallway) * amphipod.energy


def parse(line):
    return line


"""
#############
#...........#
###B#B#C#D###
  #D#C#B#A#
  #D#B#A#C#
  #D#A#A#C#
  #########"""


def run():
    lines = [
        Amphipod(4, 1, [0, 1, 2, 3], "A"),  # A
        Amphipod(8, 1, [0, 1, 2, 3], "A"),  # A
        Amphipod(9, 1, [0, 1, 2, 3], "A"),  # A
        Amphipod(14, 1, [0, 1, 2, 3], "A"),  # A
        Amphipod(3, 10, [4, 5, 6, 7], "B"),  # B
        Amphipod(5, 10, [4, 5, 6, 7], "B"),  # B
        Amphipod(7, 10, [4, 5, 6, 7], "B"),  # B
        Amphipod(10, 10, [4, 5, 6, 7], "B"),  # B
        Amphipod(11, 100, [8, 9, 10, 11], "C"),  # C
        Amphipod(12, 100, [8, 9, 10, 11], "C"),  # C
        Amphipod(13, 100, [8, 9, 10, 11], "C"),  # C
        Amphipod(6, 100, [8, 9, 10, 11], "C"),  # C
        Amphipod(0, 1000, [12, 13, 14, 15], "D"),  # D
        Amphipod(1, 1000, [12, 13, 14, 15], "D"),  # D
        Amphipod(2, 1000, [12, 13, 14, 15], "D"),  # D
        Amphipod(15, 1000, [12, 13, 14, 15], "D"),  # D
    ]
    print("solution1 = ", solution1(lines))


def render(hallway, rooms, amphipods):
    def ch(x):
        if x is None:
            return "."
        return amphipods[x].type

    a, b, c, d, e, f, g = [ch(p) for p in hallway]
    print(f"#{a}{b}.{c}.{d}.{e}.{f}{g}#")
    a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p = [ch(p) for p in rooms]
    print(f"###{d}#{h}#{l}#{p}###")
    print(f"###{c}#{g}#{k}#{o}###")
    print(f"###{b}#{f}#{j}#{n}###")
    print(f"  #{a}#{e}#{i}#{m}##\n")


def solution1(amphipods):
    amphipods.sort(key=lambda x: x.start_pos)
    gameboard = (
        [None] * HALLWAY_COUNT,
        [None] * ROOM_COUNT
    )

    for i, ap in enumerate(amphipods):
        gameboard[1][ap.start_pos] = i

    queue = []
    heapq.heappush(queue, (0, 0, next(seqnum), gameboard))
    best_solution = 1000000000
    best_score = 0
    n = 0
    visited = {}

    while queue:
        n += 1
        if n % 10000 == 0:
            print(f"{n}: score: {best_score} todo:{len(queue)}")
        _, energy, _, gameboard = heapq.heappop(queue)
        gamestate = (tuple(gameboard[0]), tuple(gameboard[1]))
        if gamestate in visited and visited[gamestate] <= energy:
            continue
        if energy >= best_solution:  # Well it ain't gonna get any better...
            continue
        visited[gamestate] = energy
        hallway, rooms = gameboard
        score = completion_score(rooms, amphipods)
        if score > best_score:
            render(hallway, rooms, amphipods)
            best_score = score
        if score == len(amphipods):
            print(f"solution {energy}")
            if energy < best_solution:
                print("BEST SO FAR!")
            best_solution = min(best_solution, energy)
            continue

        for hallway_idx, apidx in enumerate(hallway):
            if apidx is None:
                continue
            amphipod = amphipods[apidx]
            for room_idx in amphipod.rooms:
                move = make_hallway_to_room_move(amphipods, apidx, energy, hallway, hallway_idx, room_idx,
                                                 rooms, score)
                if move:
                    heapq.heappush(queue, move)

        for room_idx, apidx in enumerate(rooms):
            if apidx is None:
                continue
            amphipod = amphipods[apidx]
            # don't move if in correct place
            if room_idx == amphipod.rooms[0]:
                continue
            # look for jump straight home move
            for i in range(4):
                home = amphipod.rooms[i]
                move = make_room_to_room_move(amphipods, apidx, energy, hallway, room_idx, home, rooms, score)
                if move:
                    heapq.heappush(queue, move)
                    break
            for hallway_idx in range(HALLWAY_COUNT):
                move = make_room_to_hallway_move(amphipod, apidx, energy, hallway, hallway_idx, room_idx, rooms, score)
                if move:
                    heapq.heappush(queue, move)
    return best_solution


def make_room_to_room_move(amphipods, apidx, energy, hallway, from_room, to_room, rooms, score):
    if rooms[to_room] is not None:
        return None
    amphipod = amphipods[apidx]
    # check nothing in the way
    if not can_move_to_room(rooms, to_room, amphipod, amphipods):
        return None
    from_limit = 4 * (from_room // 4 + 1)
    hallway_idx = PATHS[from_limit][to_room > from_room]
    if hallway[hallway_idx] is not None:
        return None
    if not check_path(hallway_idx, from_room, hallway, rooms):
        return None
    if not check_path(hallway_idx, to_room, hallway, rooms):
        return None
    new_board = (hallway.copy(), rooms.copy())
    new_board[1][to_room] = apidx
    new_board[1][from_room] = None
    e = (energy,
         cost(amphipod, from_room, hallway_idx),
         cost(amphipod, to_room, hallway_idx)
         )

    return Move(score, sum(e), next(seqnum), new_board)


def make_room_to_hallway_move(amphipod, apidx, energy, hallway, hallway_idx, room_idx, rooms, score):
    # can only move to empty hallway
    if hallway[hallway_idx] is not None:
        return
    # check nothing in the way
    if not check_path(hallway_idx, room_idx, hallway, rooms):
        return
    new_board = (hallway.copy(), rooms.copy())
    new_board[0][hallway_idx] = apidx
    new_board[1][room_idx] = None
    e = energy + cost(amphipod, room_idx, hallway_idx)
    return Move(score, e, next(seqnum), new_board)


def make_hallway_to_room_move(amphipods, apidx, energy, hallway, hallway_idx, room_idx, rooms, score):
    amphipod = amphipods[apidx]
    # can only move to empty room
    if rooms[room_idx] is not None:
        return None
    # check nothing in the way
    if not check_path(hallway_idx, room_idx, hallway, rooms):
        return None
    if not can_move_to_room(rooms, room_idx, amphipod, amphipods):
        return None
    new_board = (hallway.copy(), rooms.copy())
    new_board[0][hallway_idx] = None
    new_board[1][room_idx] = apidx
    e = energy + cost(amphipod, room_idx, hallway_idx)
    return Move(score, e, next(seqnum), new_board)


def can_move_to_room(rooms, room_idx, amphipod, amphipods):
    if rooms[room_idx] != None:
        return False
    if room_idx not in amphipod.rooms:
        return False
    # room only accessible if rooms below contain correct amphipod
    limit = 4 * ((room_idx + 4) // 4 - 1)
    for i in range(limit, room_idx - 1):
        adj_ap = rooms[i]
        if adj_ap is None or amphipods[adj_ap].type != amphipod.type:
            return False
    return True


def completion_score(rooms, amphipods):
    count = 0
    for room_idx, ap in enumerate(rooms):
        if ap is None:
            continue
        amphipod = amphipods[ap]

        if is_amphipod_finished(amphipod, amphipods, room_idx, rooms):
            count += 1

    return count


def is_amphipod_finished(amphipod, amphipods, room_idx, rooms):
    if room_idx not in amphipod.rooms:
        return False
    limit = 4 * ((room_idx + 4) // 4 - 1)
    for i in range(limit, room_idx):
        adj_ap = rooms[i]
        if adj_ap is None or amphipods[adj_ap].type != amphipod.type:
            return False
    return True


def check_path(hallway_idx, room_idx, hallway, rooms):
    limit = 4 * (room_idx // 4 + 1)
    for i in range(room_idx + 1, limit):
        if rooms[i] is not None:
            return False

    path_options = PATHS[limit]

    if hallway_idx < path_options[0]:
        i = path_options[0]
        di = -1
    else:
        i = path_options[1]
        di = 1
    pathway = [hallway[i] is not None for i in range(i, hallway_idx, di)]
    if any(pathway):
        return False
    return True


if __name__ == "__main__":
    run()

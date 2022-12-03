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

# diagram
"""
#############
#01.2.3.4.56#
###1#3#5#7###
  #0#2#4#6#
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
    0: (1, 2),
    2: (2, 3),
    4: (3, 4),
    6: (4, 5)
}

"""
  0 1 2 3 4 5 6 
0 4 3 3 5 7 9 A
1 3 2 2 5 7 9 A
2 6 5 3 3 5 7 8
3 5 4 2 2 4 6 7
4 8 7 5 3 3 5 6 
5 7 6 4 2 2 4 5
6 A 9 7 5 3 3 4
7 9 8 6 4 4 2 3
"""

DISTANCES = """
4 3 3 5 7 9 A
3 2 2 5 7 9 A
6 5 3 3 5 7 8
5 4 2 2 4 6 7
8 7 5 3 3 5 6 
7 6 4 2 2 4 5
A 9 7 5 3 3 4
9 8 6 4 4 2 3
""".strip()

seqnum = count()

distances = [
    [int(v, 16) for v in line.split()]
    for line in DISTANCES.split("\n")
]

HALLWAY_COUNT = 7
ROOM_COUNT = 8
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
  #D#A#A#C#
  #########"""

def run():
    lines = [
        Amphipod(2, 1, [0, 1], "A"),  # A
        Amphipod(4, 1, [0, 1], "A"),  # A
        Amphipod(1, 10, [2, 3], "B"),  # B
        Amphipod(3, 10, [2, 3], "B"),  # B
        Amphipod(5, 100, [4, 5], "C"),  # C
        Amphipod(6, 100, [4, 5], "C"),  # C
        Amphipod(7, 1000, [6, 7], "D"),  # D
        Amphipod(0, 1000, [6, 7], "D"),  # D
    ]
    print("solution1 = ", solution1(lines))



    print("solution2 = ", solution2(lines))


def render(hallway, rooms, amphipods):
    def ch(x):
        if x is None:
            return "."
        return amphipods[x].type

    a, b, c, d, e, f, g = [ch(p) for p in hallway]
    print(f"#{a}{b}.{c}.{d}.{e}.{f}{g}#")
    a, b, c, d, e, f, g, h = [ch(p) for p in rooms]
    print(f"###{b}#{d}#{f}#{h}###")
    print(f"  #{a}#{c}#{e}#{g}##\n")


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
            if room_idx == amphipod.rooms[1]:
                other_room_occupant = rooms[amphipod.rooms[0]]
                if (
                    other_room_occupant is not None
                    and amphipods[other_room_occupant].type == amphipod.type
                ):
                    continue
            for hallway_idx in range(HALLWAY_COUNT):
                move = make_room_to_hallway_move(amphipod, apidx, energy, hallway, hallway_idx, room_idx, rooms, score)
                if move:
                    # further_move = make_hallway_to_room_move(amphipods, apidx, move.energy, hallway, hallway_idx,
                    #                                          amphipod.rooms[0], rooms, score)
                    # if further_move:
                    #     move = further_move
                    # else:
                    #     further_move = make_hallway_to_room_move(amphipods, apidx, move.energy, hallway, hallway_idx,
                    #                                              amphipod.rooms[1], rooms, score)
                    #     if further_move:
                    #         move = further_move
                    heapq.heappush(queue, move)
    return best_solution


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
    # odd rooms only accessible if valid amphipod in n-1
    if room_idx % 2:
        adj_ap = rooms[room_idx - 1]
        if adj_ap is None or amphipods[adj_ap].type != amphipod.type:
            return False
    return True


def completion_score(rooms, amphipods):
    count = 0
    for room_id, ap in enumerate(rooms):
        if ap is None:
            continue
        base_room = amphipods[ap].rooms[0]
        if rooms[base_room]:
            base_room_dweller = amphipods[rooms[base_room]]
            if base_room_dweller.type != amphipods[ap].type:
                continue
        if room_id in amphipods[ap].rooms:
            count += 1

    return count


def check_path(hallway_idx, room_idx, hallway, rooms):
    if room_idx % 2 == 0 and rooms[room_idx+1] is not None:
        return False

    path_id = room_idx - (room_idx % 2)
    path_options = PATHS[path_id]

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


def solution2(lines):
    return None


if __name__ == "__main__":
    run()

from collections import deque, defaultdict

from aocd_tools import load_input_data

EXAMPLE = """
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew""".strip()

EXAMPLE2 = """
nwwswee
ee
ww
senwse
""".strip()

DIRECTION_TABLE = {
    "ne": (0, 1, 1),
    "e": (1, 1, 0),
    "se": (1, 0, -1),
    "sw": (0, -1, -1),
    "w": (-1, -1, 0),
    "nw": (-1, 0, 1)
}


def parse(line):
    result = []
    line = deque([ch for ch in line])
    while line:
        token = ""
        while token not in DIRECTION_TABLE:
            token += line.popleft()
        result.append(DIRECTION_TABLE[token])
    return deque(result)


def run():
    input_data = load_input_data(2020, 24)
    input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    lines = process_input(input_data)
    print(lines)
    print("solution1 = ", solution1(lines))
    print("solution2 = ", solution2(lines))


def process_input(input_data):
    return deque([parse(line) for line in input_data.split("\n")])


class Tile:
    def __init__(self):
        self.is_white = True

    @property
    def colour(self):
        return "white" if self.is_white else "black"


def solution1(lines):
    tiles = defaultdict(Tile)

    print(f"Found {len(lines)} lines")
    for directions in lines:
        pos = (0, 0, 0)
        for move in directions:
            pos = add_vectors(pos, move)
            # print(f"Move to {pos}")
        tiles[pos].is_white = not tiles[pos].is_white

        print(f"Flipped {pos} to {tiles[pos].colour}")

    return len([t for t in tiles.values() if not t.is_white])


def add_vectors(a, b):
    return tuple([v1+v2 for v1, v2 in zip(a, b)])


def solution2(lines):
    return


if __name__ == "__main__":
    run()

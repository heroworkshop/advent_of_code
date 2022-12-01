from collections import defaultdict, namedtuple

from input_data.day4 import INPUT_DATA


EXAMPLE = """
aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]""".strip()

Room = namedtuple("room", "name sector_id checksum")


def parse(line):
    line, _, checksum = line[:-1].partition("[")
    name, _, sector_id = line.rpartition("-")

    return Room(name, int(sector_id), checksum)


def run():
    input_data = [parse(line) for line in INPUT_DATA.split("\n")]
    print("solution1=", solution1(input_data))
    print("solution2=", solution2(input_data))


def solution1(input_data):
    total = 0
    for room in input_data:
        print(room, end=" ")
        if is_a_room(room):
            total += room.sector_id
            print("Is a room")
        else:
            print("Is not a room")
    return total


def is_a_room(room):
    tally = tally_characters(room.name)
    checksum = most_common(tally, 5)
    return checksum == room.checksum


def tally_characters(name):
    tally = defaultdict(int)
    for ch in name:
        if ch != "-":
            tally[ch] += 1
    return tally


def most_common(tally, count):
    result = []
    while len(result) < count:
        f_max = max(tally.values())
        candidates = [k for k, v in tally.items() if v == f_max]
        candidates.sort()
        first = candidates[0]
        result.append(first)
        del tally[first]
    return "".join(result)


def solution2(input_data):
    for room in input_data:
        if is_a_room(room):
            name = decrypt_name(room)
            print(name)
            if name == "northpole object storage":
                return room.sector_id


def decrypt_name(room):
    symbols = "abcdefghijklmnopqrstuvwxyz"
    result = []
    for ch in room.name:
        if ch == "-":
            result.append(" ")
        else:
            i = symbols.index(ch)
            result.append(symbols[(i + room.sector_id) % len(symbols)])
    return "".join(result)


if __name__ == "__main__":
    run()

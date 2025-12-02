from y2025.day02_data import DATA

EXAMPLE = """
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124
"""

def parse(data):
    lines = [line.strip() for line in data.strip().split(",")]
    return lines


def part1():
    result = 0
    rows = parse(DATA)
    for row in rows:
        parts = row.split("-")
        start, end = int(parts[0]), int(parts[1])
        for n in range(start, end + 1):
            s = str(n)
            len(s) // 2
            if len(s) % 2 != 0:
                continue
            mid = len(s) // 2
            left = s[:mid]
            right = s[mid:]
            if left == right:
                result += int(n)

    return result


def part2():
    result = 0
    rows = parse(DATA)
    for row in rows:
        parts = row.split("-")
        start, end = int(parts[0]), int(parts[1])
        print(start, " to ", end)
        for n in range(start, end + 1):
            s = str(n)
            if is_invalid(s):
                print(n)
                result += int(n)

    return result


def is_invalid(s: str) -> bool:
    longest = (len(s) // 2)
    for divider in range(1, longest + 1):
        if len(s) % divider != 0:
            continue
        segments = split_into_segments(s, divider)
        if len(segments) == 1:
            return False
        if all_equal(segments):
            return True
    return False


def split_into_segments(s, segment_length):
    result = []
    while s:
        result.append(s[:segment_length])
        s = s[segment_length:]
    return result


def all_equal(lst):
    return all(x == lst[0] for x in lst)


if __name__ == "__main__":
    print("part1:", part1())
    print("part2:", part2())
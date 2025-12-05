from y2025.day05_data import DATA

EXAMPLE = """
3-5
10-14
16-20
12-18

1
5
8
11
17
32
""".strip()

def parse(data):
    lines = [line.strip() for line in data.strip().split("\n\n")]
    return lines


def part1():
    result = 0
    fresh_str, rows_str = parse(DATA)
    fresh_range = parse_range(fresh_str.split("\n"))
    for row in rows_str.split("\n"):
        if is_fresh(int(row),  fresh_range):
            result += 1
    return result


def set_from_ranges(lines: list[str]) -> set[int]:
    result = set()
    for item in lines:
        start, end = [int(x) for x in item.split("-")]
        for v in range(start, end + 1):
            result.add(v)
    return result



def part2():
    fresh_str, rows_str = parse(DATA)
    fresh_ranges = parse_range(fresh_str.split("\n"))

    merged = merge_ranges(fresh_ranges)
    result = sum(
        end - start + 1
        for start, end in merged
    )

    return result

IntegerRange = tuple[int, int]

def merge_ranges(ranges: list[IntegerRange]) -> list[IntegerRange]:
    """Merges overlapping or contiguous ranges

    Example:
    >>> merge_ranges([(3,5), (10,14), (16,20), (12,18)])
    [(3, 5), (10, 20)]

    """
    if not ranges:
        return []
    # Sort ranges by start value
    sorted_ranges = sorted(ranges, key=lambda x: x[0])
    merged = [sorted_ranges[0]]

    for current in sorted_ranges[1:]:
        last_start, last_end = merged[-1]
        current_start, current_end = current

        if current_start <= last_end + 1:  # Overlapping or contiguous ranges
            merged[-1] = (last_start, max(last_end, current_end))
        else:
            merged.append(current)

    return merged

def parse_range(lines: list[str]) -> list[IntegerRange]:
    """Parses lines like '3-5' into list of (3,5)"""
    result = []
    for item in lines:
        start, end = [int(x) for x in item.split("-")]
        result.append((start, end))
    return result

def is_fresh(value: int, ranges: list[tuple[int, int]]) -> bool:
    for start, end in ranges:
        if start <= value <= end:
            return True
    return False


if __name__ == "__main__":
    print("part1:", part1())
    print("part2:", part2())

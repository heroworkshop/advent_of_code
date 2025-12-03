from y2025.day03_data import DATA

EXAMPLE = """
987654321111111
811111111111119
234234234234278
818181911112111
"""

def parse(data):
    lines = [
        [
            int(ch) for ch in
            line.strip()
        ]
        for line in data.strip().splitlines()
    ]
    return lines


def part1():
    result = 0
    rows = parse(DATA)
    for row in rows:
        # print (row)
        m = max(row[:-1])
        # print(m)
        p = row.index(m)
        # print(p)
        m2 = max(row[p+1:])
        # print(m2)
        total = m * 10 + m2
        print(total)
        result += total
    return result


def part2():
    result = 0
    rows = parse(DATA)
    for row in rows:
        n_str = ""
        for n in range(12, 0, -1):
            remaining = n - 1
            print("n_str=", n_str, " remaining=", remaining, " row=", row)
            m = max(row[:-remaining] if remaining else row)
            n_str += str(m)
            row = row[row.index(m)+1:]
        v = int(n_str)
        print("v=", v)
        result += v


    return result


if __name__ == "__main__":
    print("part1:", part1())
    print("part2:", part2())

from y2025.day1_data import DATA


EXAMPLE = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""

def part1():
    p = 50
    total = 0
    for line in DATA.split("\n"):
        d = line[0]
        a = int(line[1:])
        if d == "R":
            p += a
        elif d == "L":
            p -= a
        p = p % 100
        if p == 0:
            total += 1
    return total

def part2():
    p = 50
    total = 0
    for line in DATA.split("\n"):
        d = line[0]
        a = int(line[1:])
        di = -1 if d == "L" else 1
        for _ in range(a):
            p += di
            p = p % 100
            if p == 0:
                total += 1
    return total


if __name__ == "__main__":
    print("part1:", part1())
    print("part2:", part2())

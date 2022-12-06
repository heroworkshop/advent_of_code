from collections import defaultdict, deque

from aocd_tools import load_input_data


def parse(line):
    return int(line)


def run():
    input_data = load_input_data(2021, 6)
    print(f"loaded input data ({len(input_data)} bytes)")
    # input_data = "3,4,3,1,2"
    lines = [parse(line) for line in input_data.split(",")]
    print("solution1 = ", solution1(lines))
    print("solution2 = ", solution2(lines))


def solution1(fish):
    for day in range(80):
        next_gen = []
        for f in fish:
            f -= 1
            if f == -1:
                f = 6
                next_gen.append(8)
            next_gen.append(f)
        fish = next_gen
    return len(fish)


def solution2_bf(fish):
    for day in range(256):
        next_gen = []
        for f in fish:
            f -= 1
            if f == -1:
                f = 6
                next_gen.append(8)
            next_gen.append(f)
        fish = next_gen
        print(day, len(fish))
    return len(fish)


def model_growth1(fish):
    days = 256
    fish_by_day = defaultdict(list)
    count = 0
    fish_by_day[0].extend(fish)
    for day in range(days + 1):
        count += len(fish_by_day[day])
        for f in fish_by_day[day]:
            # Add new fish at appropriate days
            # e.g if f is 3, add at:
            # day + f + 1,
            # day + f + 1 + 7, ...
            # a total of 1 + (MAXDAY - d)//7 fish
            future = day + f + 1
            while True:
                if future > days:
                    break
                fish_by_day[future].append(8)
                future += 7
        print(day, count)
    return count


def solution2(fish):
    days = 256
    d = deque([0] * 9)
    for f in fish:
        d[f] += 1
    for _ in range(days):
        d.append(d.popleft())  # create a new lanternfish with an internal timer of 8
        d[6] += d[-1]  # zero-timer fish internal timer would reset to 6
        print(d)
    return sum(d)


if __name__ == "__main__":
    run()

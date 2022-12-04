from aocd_tools import load_input_data

EXAMPLE = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""


def integerise(slist):
    return [int(x) for x in slist]


def simplify(entries):
    if all(len(e) == 1 for e in entries):
        return [line[0] for line in entries]
    return entries

def rucksack(contents):
    size = len(contents) // 2
    left = contents[:size]
    right = contents[size:]
    return left, right


def common(pair):
    left, right = pair
    left = set(c for c in left)
    right = set(c for c in right)
    matching = left & right
    return matching.pop()

def priority(v):
    if v in "qwertyuiopasdfghjklzxcvbnm":
        return ord(v) - ord('a') + 1
    return ord(v) - ord("A") + 27


def run():
    input_data = load_input_data(2022, 3)
    # input_data = EXAMPLE

    print(f"loaded input data ({len(input_data)} bytes)")

    entries = input_data.split("\n")
    rucksacks = [rucksack(e) for e in entries]
    common_items = [common(p) for p in rucksacks]
    print(common_items)
    values = [priority(i) for i in common_items]
    print([a for a in zip(common_items, values)])

    # print(entries[:50])

    print("solution1 = ", sum(values))

    total = 0
    for a,b,c in zip(entries[::3], entries[1::3], entries[2::3]):
        print(f"{a}-{b}-{c}")
        badge = set(a) & set(b) & set(c)
        print(badge)
        total += priority(badge.pop())
    print("solution2 = ", total)


def solution1(entries):
    return ""


def solution2(entries):
    return ""


if __name__ == "__main__":
    run()

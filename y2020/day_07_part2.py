from collections import namedtuple

from aocd_tools import load_input_data


EXAMPLE = """
shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.""".strip()

BagRule = namedtuple("bag_rule", "colour count")


def run():
    input_data = load_input_data(2020, 7)
    # input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    print("solution2 = ", solution2(input_data.split("\n")))


def parse_rules(line):
    key, _, contains = line.partition(" contain ")
    key, _, _ = key.partition(" bag")
    values = []
    if "no other bags" not in contains:
        for field in contains.split(","):
            field = field.strip()
            count, _, field = field.partition(" ")
            count = int(count)
            colour, _, _ = field.partition(" bag")
            values.append(BagRule(colour, count))

    return key.strip(), values


def count_containing(colour, rules):
    queue = [(1, colour)]
    count = 0

    while queue:
        n, colour = queue.pop(0)
        contains = rules[colour]
        count += n
        for bag in contains:
            queue.append((bag.count * n, bag.colour))
    return count - 1


def solution2(lines):
    bag_rules = {}
    for line in lines:
        k, v = parse_rules(line)
        bag_rules[k] = v

    return count_containing("shiny gold", bag_rules)


if __name__ == "__main__":
    run()

from aocd_tools import load_input_data


def run():
    input_data = load_input_data(2020, 7)
    print(f"loaded input data ({len(input_data)} bytes)")
    print("solution1 = ", solution1(input_data.split("\n")))
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
            values.append(colour)

    return key.strip(), values


def find_containing(colour, rules):
    queue = [colour]
    result = set()

    while queue:
        colour = queue.pop(0)
        for bag, contains in rules.items():
            if colour in contains:
                result.add(bag)
                queue.append(bag)
    return result


def solution1(lines):
    bag_rules = {}
    for line in lines:
        k, v = parse_rules(line)
        bag_rules[k] = v

    return len(find_containing("shiny gold", bag_rules))


def solution2(lines):
    return


if __name__ == "__main__":
    run()

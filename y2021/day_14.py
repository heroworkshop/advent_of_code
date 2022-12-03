from collections import defaultdict, namedtuple, Counter
from functools import cache
from pprint import pprint

from aocd_tools import load_input_data


EXAMPLE = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""

Rule = namedtuple("rule", "pair insert")


def parse(line):
    return Rule(*(line.split(" -> ")))


def run():
    input_data = load_input_data()
    # input_data  = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    initial, rules = input_data.split("\n\n")
    rules = [parse(rule) for rule in rules.split("\n")]
    rules = {rule.pair: rule.insert for rule in rules}
    # lines = grid_from_lines(input_data, transform=int)
    print("solution1 = ", solution1(initial, rules))


def do_subs(chain, rules):
    result = chain[0]
    for a, b in zip(chain[:-1], chain[1:]):
        i = rules.get(a + b, "")
        result += i + b
    return result


def solution1_slow(chain, rules):
    for i in range(40):
        chain = do_subs(chain, rules)
        print(i, len(chain))
    c = Counter(chain)
    low = min(c.values())
    hi = max(c.values())
    return hi - low

def solution1(chain, rules):
    counts = defaultdict(int)
    for a, b in zip(chain[:-1], chain[1:]):
        counts[a+b] += 1

    for i in range(40):
        new_counts = defaultdict(int)
        for pair, n in counts.items():
            a, b = pair
            if pair in rules:
                c = rules[pair]
                new_counts[a+c] += n
                new_counts[c+b] += n
            else:
                new_counts[a+b] += n
        counts = new_counts
        print(i, sum(counts.values()) + 1)

    pprint(counts)
    elem_counts = defaultdict(int)
    for pair, n in counts.items():
        a, b = pair
        elem_counts[a] += n
    elem_counts[chain[-1]] += 1
    return max(elem_counts.values()) - min(elem_counts.values())


if __name__ == "__main__":
    run()

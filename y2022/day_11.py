from collections import deque
from dataclasses import dataclass
from typing import NamedTuple, List

from aocd_tools import load_input_data


EXAMPLE = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""

@dataclass
class Monkey:
    items: deque[int]
    operation: str
    modulo_test: int
    throw_true: int
    throw_false: int
    inspection_count: int = 0

    def process_items(self, monkeys, divisor, super_modulo):

        while self.items:
            old = self.items.popleft()
            self.inspection_count += 1
            new = eval(self.operation) % super_modulo
            item = new // divisor
            target = self.throw_false if item % self.modulo_test else self.throw_true
            monkeys[target].items.append(item)



def run():
    input_data = load_input_data(2022, 11)
    #input_data = EXAMPLE

    print(f"loaded input data ({len(input_data)} bytes)")

    monkeys = input_data.split("\n\n")
    monkeys = [parse(line) for line in monkeys]
    print(monkeys[:50])

   # print("solution1 = ", solution1(monkeys))

    print("solution2 = ", solution2(monkeys))


def parse(lines: str):
    lines = lines.split("\n")
    starting_items = items_from_str(lines[1])
    _, _, operation = lines[2].partition("=")
    return Monkey(items=deque(starting_items), operation=operation.strip(),
                  modulo_test=extract_last_int(lines[3]),
                  throw_true=extract_last_int(lines[4]),
                  throw_false=extract_last_int(lines[5]))


def extract_last_int(line):
    return int(line.split()[-1])


def items_from_str(line):
    parts = line.split()
    return [int(part.replace(",", "")) for part in parts[2:]]

def solution1(monkeys):
    super_modulo = 1
    for monkey in monkeys:
        super_modulo *= monkey.modulo_test
    for _ in range(1, 21):
        for monkey in monkeys:
            monkey.process_items(monkeys, 3, super_modulo)

    counts = [monkey.inspection_count for monkey in monkeys]
    counts = sorted(counts)
    return counts[-1] * counts[-2]


def solution2(monkeys):
    super_modulo = 1
    for monkey in monkeys:
        super_modulo *= monkey.modulo_test
    muls = " * ".join([str(monkey.modulo_test) for monkey in monkeys])
    print(f"{muls} = {super_modulo}")
    for r in range(1, 10001):
        if r % 1000 == 0:
            print(f"Round {r}")
            print(monkey_counts(monkeys))
        for monkey in monkeys:
            monkey.process_items(monkeys, 1, super_modulo)


    counts = monkey_counts(monkeys)
    counts = sorted(counts)
    return counts[-1] * counts[-2]


def monkey_state(monkeys):
    state = []
    for monkey in monkeys:
        state.extend(monkey.items)
    return tuple(state)

def monkey_counts(monkeys):
    return tuple([monkey.inspection_count for monkey in monkeys])


if __name__ == "__main__":
    run()

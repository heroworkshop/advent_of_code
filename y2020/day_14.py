from collections import defaultdict
from copy import copy

from aocd_tools import load_input_data


class Computer:
    def __init__(self):
        self.memory = defaultdict(int)
        self.mask = dict()

    def run(self, program):
        for lhs, rhs in program:
            if lhs.startswith("mask"):
                self.update_mask(rhs)
            elif lhs.startswith("mem"):
                self.update_mem(int(lhs[4:-1]), int(rhs), self.mask)
            else:
                raise ValueError(f"Invalid command {lhs}")

    def update_mask(self, value: str):
        print(f"update mask {value}")
        mask = dict()
        for i, bit in enumerate(reversed(value)):
            if bit != "X":
                mask[i] = int(bit)
        print(mask)
        self.mask = mask

    def update_mem(self, address, value, mask):
        print(f"update mem {address}", end="")
        value = self.apply_mask(mask, value)
        print(f"-> {value}")

        self.memory[address] = value

    @staticmethod
    def apply_mask(mask, value):
        for i, bit in mask.items():
            if bit:
                value = value | (1 << i)
            else:
                value = value & ~(1 << i)
        return value


class ComputerMk2(Computer):
    def __init__(self):
        super().__init__()
        self.floating_bits = set()

    def update_mask(self, value: str):
        print(f"update mask {value}")
        mask = dict()
        floating_bits = list()
        for i, bit in enumerate(reversed(value)):
            if bit == "X":
                floating_bits.append(i)
            else:
                mask[i] = int(bit)
        print(mask)
        print(floating_bits)
        self.mask = mask
        self.floating_bits = floating_bits

    def update_mem(self, address, value, mask):
        if not len(self.floating_bits):
            super.update_mem(self.apply_mask(mask, address), value, {})
            return
        base_address = self.apply_mask(mask, address)
        for floater in range(1 << len(self.floating_bits)):
            address = base_address
            for i, offset in enumerate(self.floating_bits):
                if (floater >> i) & 1:
                    address = address | (1 << offset)
                else:
                    address = address & ~(1 << offset)
            # print(f"{base_address:b} -> {address:b}")
            super().update_mem(address, value, {})

    @staticmethod
    def apply_mask(mask, value):
        for i, bit in mask.items():
            if bit:
                value = value | (1 << i)
            else:
                pass
        return value

def parse_line(line):
    lhs, _, rhs = line.partition("=")

    return lhs.strip(), rhs.strip()


def parse(input_data):
    return [parse_line(line) for line in input_data.split("\n")]


def run():
    input_data = load_input_data(2020, 14)
    print(f"loaded input data ({len(input_data)} bytes)")
    lines = parse(input_data)
    print("solution1 = ", solution1(lines))
    print("solution2 = ", solution2(lines))


def solution1(program):
    computer = Computer()
    computer.run(program)

    return sum(computer.memory.values())


def solution2(program):
    computer = ComputerMk2()
    computer.run(program)

    return sum(computer.memory.values())


if __name__ == "__main__":
    run()

import heapq
import re
from aocd_tools import *


EXAMPLE = """
"""

class InvalidRun(Exception):
    pass

def run():
    for i, f in enumerate((solution1, solution2), 1):
        start_time = time.process_time()
        print(f"solution{i} = ", f(), time_report(start_time))

def instructions_parse(instructions):
    return tuple(int(v) for v in instructions.split(","))


def solution1():
    ex1 = Device(729, 0,0, instructions_parse("0,1,5,4,3,0"))
    print(ex1.run())
    dev = Device(66752888, 0, 0, instructions_parse("2,4,1,7,7,5,1,7,0,3,4,1,5,5,3,0"))
    return dev.run()

def solution2():
    prog = instructions_parse("2,4,1,7,7,5,1,7,0,3,4,1,5,5,3,0")
    queue = []
    heapq.heappush(queue, (0, "111"))
    while queue:
        score, v = heapq.heappop(queue)
        a = v + "0"
        b = v + "1"
        for s in (a, b):
            i = int(s, 2)
            dev = Device(i, 0, 0, prog)
            result = dev.run()
            print(s, result)
            if result == prog:
                return i
            score = len(prog) - count_rmatches(result, prog)
            heapq.heappush(queue, (score, s))
    return 0

def count_rmatches(lhs, rhs):
    count = 0
    for a, b in zip(lhs[-1::-1], rhs[-1::-1]):
        if a == b:
            count += 1
    return count

class Device:
    def __init__(self, a: int, b:int, c:int, instructions: tuple[int, ...]):
        self.a, self.b, self.c = a,b,c
        self.instructions = instructions
        self.pc = 0
        self.output = []

    def run(self):
        while True:
            try:
                opcode = self.instructions[self.pc]
                operand = self.instructions[self.pc + 1]
            except IndexError:
                break
            try:
                self.op(opcode, operand)
            except InvalidRun:
                return ""
            self.pc += 2
        return self.output

    def combo(self, operand):
        return (0, 1, 2, 3, self.a, self.b, self.c)[operand]

    def adv(self, operand):
        self.a = self.a // 2 ** self.combo(operand)

    def bxl(self, operand):
        self.b = self.b ^ operand

    def bst(self, operand):
        self.b = self.combo(operand) % 8

    def jnz(self, operand):
        if self.a:
            self.pc = operand - 2

    def bxc(self, operand):
        self.b = self.b ^ self.c

    def out(self, operand):
        self.output.append(self.combo(operand) % 8)

    def bdv(self, operand):
        self.b = self.a // 2 ** self.combo(operand)

    def cdv(self, operand):
        self.c = self.a // 2 ** self.combo(operand)

    def op(self, opcode, operand):
        f = (self.adv, self.bxl, self.bst, self.jnz, self.bxc, self.out, self.bdv, self.cdv)[opcode]
        f(operand)


class DupDevice(Device):
    def out(self, operand):
        outv = self.combo(operand) % 8
        offset = len(self.output)
        if offset > len(self.instructions) or outv != self.instructions[offset]:
            raise InvalidRun
        self.output.append(outv)


def extract_lines(entries):
    return entries.split("\n")


if __name__ == "__main__":
    run()

from collections import defaultdict, deque
from contextlib import suppress


class Chip:
    def __init__(self, assembly_code):
        self.registers = defaultdict(int)
        self.last_sound = 0
        self.program = self.compile(assembly_code)
        self.pc = 0

        self.running = False

    @staticmethod
    def interpret_param(p):
        with suppress(ValueError):
            p = int(p)
        return p

    def evaluate(self, param):
        if isinstance(param, int):
            return param
        return self.registers.get(param, 0)


    def compile_line(self, line):
        operations = {
            "snd": self.play_sound,
            "set": self.set,
            "add": self.add,
            "mul": self.mul,
            "mod": self.mod,
            "rcv": self.recover,
            "jgz": self.jump,
        }
        op_code, *args = line.split()
        return operations[op_code], *args

    def compile(self, code):

        program = [self.compile_line(line)
                   for line_number, line in enumerate(code.split("\n"))
]
        return program

    def play_sound(self, freq):
        self.last_sound = self.evaluate(freq)

    def set(self, x, y):
        self.registers[x] = self.evaluate(y)

    def add(self, x, y):
        self.registers[x] += self.evaluate(y)

    def mul(self, x, y):
        self.registers[x] *= self.evaluate(y)

    def mod(self, x, y):
        self.registers[x] = self.registers[x] % self.evaluate(y)

    def jump(self, x, y):
        if self.evaluate(x) > 0:
            self.pc += self.evaluate(y) - 1

    def run(self):
        self.running = True
        self.pc = 0
        while self.running:
            try:
                op, *params = self.program[self.pc]
                params = [self.interpret_param(p) for p in params]
                op(*params)
            except IndexError:
                return
            self.pc += 1


class SoundChip(Chip):
    def __init__(self, assembly_code, on_recover=None):
        super().__init__(assembly_code)
        self.on_recover = on_recover

    def recover(self, x):
        if not self.evaluate(x):
            return
        if self.on_recover:
            self.on_recover(self)


class ConnectedChip(Chip):
    def __init__(self, assembly_code, pid):
        super().__init__(assembly_code)
        self.buffer = deque()
        self.connected = None
        self.locked = False
        self.p = pid

    def connect(self, chip):
        self.connected = chip

    def recover(self, x):
        while not self.buffer:
            self.locked = True
            if self.connected.locked:
                self.running = False
                self.connected.running = False
                return
        self.locked = False
        self.registers[x] = self.buffer.popleft()

    def play_sound(self, x):
        if self.connected:
            self.connected.buffer.append(self.evaluate(x))

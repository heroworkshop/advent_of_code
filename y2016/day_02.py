from input_data.day2 import INPUT_DATA

DIRECTIONS = {"R": (1, 0), "D": (0, 1), "L": (-1, 0), "U": (0, -1)}

PAD1 = """
123
456
789""".strip()


PAD2 = """
  1
 234
56789
 ABC
  D"""


def make_numpad_keys(lines):
    x, y = 0, 0
    start = None
    result = {}
    for line in lines.split("\n"):
        for ch in line:
            if ch != " ":
                result[(x, y)] = ch
            if ch == "5":
                start = (x, y)
            x += 1
        x = 0
        y += 1
    return result, start


class NumPad:
    def __init__(self, keys):
        self.numpad_keys, self.p = make_numpad_keys(keys)

    def move(self, v):
        x, y = self.p
        x += v[0]
        y += v[1]
        if (x, y) in self.numpad_keys:
            self.p = x, y

    def run(self, instructions):
        for v in instructions:
            self.move(v)

    def current_key(self):
        return self.numpad_keys[self.p]


def parse(line):
    return [DIRECTIONS[ch] for ch in line]


def run():
    input_data = [parse(line) for line in INPUT_DATA.split("\n")]
    print("solution1=", solution1(input_data))
    print("solution2=", solution2(input_data))


def solution1(input_data):
    numpad = NumPad(PAD1)
    result = []
    for line in input_data:
        numpad.run(line)
        result.append(numpad.current_key())

    return "".join(result)


def solution2(input_data):
    numpad = NumPad(PAD2)
    result = []
    for line in input_data:
        numpad.run(line)
        result.append(numpad.current_key())

    return "".join(result)


if __name__ == "__main__":
    run()

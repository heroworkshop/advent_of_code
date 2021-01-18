from aocd_tools import load_input_data

EXAMPLE = "3, 4, 1, 5"


class CircularBuffer:
    def __init__(self, length):
        self.length = length
        self.values = [i for i in range(length)]

    def reverse(self, start, end):
        while start < end:
            a, b = self.actual(start), self.actual(end)
            self.values[a], self.values[b] = self.values[b], self.values[a]
            start += 1
            end -= 1

    def actual(self, index):
        return index % self.length

    def at(self, index):
        return self.values[self.actual(index)]

    def render(self, highlight_index):
        highlight_index = self.actual(highlight_index)
        parts = [f"[{v}]" if i == highlight_index else f"{v}"
                 for i, v in enumerate(self.values)]
        return " ".join(parts)


def parse(line):
    return int(line)


def run():
    input_data = load_input_data(2017, 10)
    # input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    lines = [parse(line) for line in input_data.split(",")]
    print("solution1 = ", solution1(lines))
    print("solution2 = ", solution2(input_data))


def solution1(lines):
    values = CircularBuffer(256)
    p = 0
    step = 0
    print(values.render(p))
    for n in lines:
        values.reverse(p, p + n - 1)
        p += step + n
        step += 1
        print(values.render(p))
    return values.at(0) * values.at(1)


def solution2(input_data):
    lines = [ord(ch) for ch in input_data]
    lines.extend([17, 31, 73, 47, 23])
    values = CircularBuffer(256)
    p = 0
    step = 0
    for round in range(64):
        for n in lines:
            values.reverse(p, p + n - 1)
            p += step + n
            step += 1
            print(values.render(p))

    hash = dense_hash(values)
    return "".join([f"{c:02x}" for c in hash])


def dense_hash(values):
    result = [values.at(n*16) for n in range(16)]
    for n in range(16):
        for m in range(1,16):
            k = values.at(n*16 + m)
            result[n] ^= k
    return result


if __name__ == "__main__":
    run()

from aocd_tools import load_input_data


def run():
    input_data = load_input_data(2021, 4)
    print(f"loaded input data ({len(input_data)} bytes)")

    called_numbers, boards = parse_cmds(input_data)

    print("solution1 = ", solution1(called_numbers, boards))
    print("solution2 = ", solution2(called_numbers, boards))


class Board:
    def __init__(self, lines):
        self.all_numbers: set = set()
        self.rows = []
        self.cols = [set() for _ in range(5)]
        for line in lines:
            numbers = [int(n) for n in line.split()]
            self.all_numbers.update(set(numbers))
            self.rows.append(set(numbers))
            for x, n in enumerate(numbers):
                self.cols[x].add(n)

        self.called_numbers = set()

    def sum_of_remaining(self):
        return sum(self.all_numbers.difference(self.called_numbers))

    def call_number(self, n):
        self.called_numbers.add(n)
        for r in self.rows:
            r.discard(n)
        for c in self.cols:
            c.discard(n)

    def bingo(self):
        for r in self.rows:
            if not r:
                return True
        for c in self.cols:
            if not c:
                return True
        return False


def parse_cmds(input_data):
    lines = input_data.split("\n")
    called_numbers = [int(x) for x in lines[0].split(",")]
    boards = [Board(lines[n:n+5]) for n in range(2, len(lines), 6)]
    return called_numbers, boards



def solution1(called_numbers, boards):
    for n in called_numbers:
        for b in boards:
            b.call_number(n)
            if b.bingo():

                return b.sum_of_remaining() * n
    return 0


def solution2(called_numbers, boards):
    for n in called_numbers:
        for b in boards:
            b.call_number(n)
        score = boards[0].sum_of_remaining() * n
        boards = [b for b in boards if not b.bingo()]
        if not boards:
            return score
    return 0


if __name__ == "__main__":
    run()

from collections import deque

from aocd_tools import load_input_data


class Node:
    def __init__(self, parent):
        self.parent = parent
        self.children = []
        parent_score = parent.score if parent else 0
        self.score = parent_score + 1
        if parent:
            parent.children.append(self)

    def parse(self, it):
        while True:
            ch = next(it)
            if ch == "{":
                child = Node(self)
                child.parse(it)
            elif ch == "}":
                return

    def count(self):
        return self.score + sum([c.count() for c in self.children])


def parse(line):
    return int(line)


def run():
    input_data = load_input_data(2017, 9)
    print(f"loaded input data ({len(input_data)} bytes)")

    print("solution1 = ", solution1(input_data))
    print("solution2 = ", solution2(input_data))


def solution1(input_data):
    unescaped = unescape(input_data, "!")
    cleaned = remove_garbage(unescaped)
    tree = make_tree(cleaned)
    return tree.count()


def unescape(src, escape_char):
    result = []
    src = deque(src)
    while src:
        ch = src.popleft()
        if ch == escape_char:
            src.popleft()
        else:
            result.append(ch)
    return "".join(result)


def remove_garbage(src):
    src = deque(src)
    result = []
    garbage_count = 0
    while src:
        ch = src.popleft()
        if ch == "<":
            while ch != ">":
                ch = src.popleft()
                if ch != ">":
                    garbage_count += 1
        else:
            result.append(ch)

    print("Garbage count = ", garbage_count)
    return "".join(result)


def make_tree(stream):
    it = iter(stream)
    while True:
        ch = next(it)
        if ch == "{":
            root = Node(None)
            root.parse(it)
            return root


def solution2(input_data):
    return


if __name__ == "__main__":
    run()

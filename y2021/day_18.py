import json
import math
from collections import defaultdict, namedtuple
from contextlib import suppress
from itertools import combinations, chain

from aocd_tools import load_input_data
from pyparsing import OneOrMore, nestedExpr

EXAMPLE = """"""


class SnailfishNumber:
    def __init__(self, tree_as_list, parent=None, level=0):
        self.parent = parent
        self.level = level
        self.right = None
        if isinstance(tree_as_list[0], list):
            self.left = SnailfishNumber(tree_as_list[0], self, level + 1)
        else:
            self.left = tree_as_list[0]
        if isinstance(tree_as_list[1], list):
            self.right = SnailfishNumber(tree_as_list[1], self, level + 1)
        else:
            self.right = tree_as_list[1]

    def add_left(self, i):
        if isinstance(self.left, int):
            self.left += i
            return
        node = self.find_left_branch()
        if not node:
            return
        if isinstance(node.left, int):
            self.left += i
            return
        node.left.add_right_child_int(i)

    def add_right(self, i):
        if isinstance(self.right, int):
            self.right += i
            return
        node = self.find_right_branch()
        if not node:
            return
        if isinstance(node.right, int):
            node.right += i
            return
        node.right.add_left_child_int(i)

    def add_left_child_int(self, i):
        if isinstance(self.left, int):
            self.left += i
            return True
        if self.left.add_left_child_int(i):
            return True
        return self.right.add_left_child_int(i)

    def add_right_child_int(self, i):
        if isinstance(self.right, int):
            self.right += i
            return True
        if self.right.add_right_child_int(i):
            return True
        return self.right.add_right_child_int(i)

    def find_right_branch(self):
        if not self.parent:
            return None
        if self.parent.right != self:
            return self.parent
        return self.parent.find_right_branch()

    def find_left_branch(self):
        if not self.parent:
            return None
        if self.parent.left != self:
            return self.parent
        return self.parent.find_left_branch()

    def explode_left(self):
        self.add_right(self.left.right)
        self.parent.add_left(self.left.left)
        self.left = 0

    def explode_right(self):
        self.add_left(self.right.left)
        self.parent.add_right(self.right.right)
        self.right = 0

    def render(self):
        left = self.left if isinstance(self.left, int) else self.left.render()
        right = self.right if isinstance(self.right, int) else self.right.render()
        return f"[{left},{right}]"

    def explode(self):
        if self.parent.left == self:
            self.parent.explode_left()
        else:
            self.parent.explode_right()

    def find_first_level4(self):
        node = None
        if self.level == 4:
            return self
        if not isinstance(self.left, int):
            node = self.left.find_first_level4()
        if not node and not isinstance(self.right, int):
            node = self.right.find_first_level4()
        return node

    def split_first(self):
        if isinstance(self.left, int):
            if self.left > 9:
                left = math.floor(self.left / 2)
                right = math.ceil(self.left / 2)
                self.left = SnailfishNumber([left, right], self, self.level + 1)
                return True
        else:
            if self.left.split_first():
                return True
        if isinstance(self.right, int):
            if self.right > 9:
                left = math.floor(self.right / 2)
                right = math.ceil(self.right / 2)
                self.right = SnailfishNumber([left, right], self, self.level + 1)
                return True
        else:
            if self.right.split_first():
                return True
        return False

    def reduce(self):
        reducing = True
        while reducing:
            node = self.find_first_level4()
            if node:
                node.explode()
                continue
            if not self.split_first():
                reducing = False

    def magnitude(self):
        a = self.left if isinstance(self.left, int) else self.left.magnitude()
        b = self.right if isinstance(self.right, int) else self.right.magnitude()
        return a * 3 + b * 2


def make_snailfish_number(line):
    parsed = json.loads(line)
    return SnailfishNumber(parsed)


def make_snailfish_list(line):
    def safe_int(i):
        with suppress(ValueError):
            return int(i)
        return i

    return [safe_int(x) for x in line]


def explode(sf_list):
    level = -1
    for p, x in enumerate(sf_list):
        if x == "[":
            level += 1
            if level == 4:
                explode_at(p, sf_list)
                return True
        elif x == "]":
            level -= 1
    return False


def sf_list_to_str(sf_list):
    return "".join([str(s) for s in sf_list])


def explode_at(p, sf_list):
    p1 = sf_list.index("]", p)
    explode_str = sf_list_to_str(sf_list[p:p1])
    v1, v2 = [int(v) for v in explode_str.strip("[]").split(",")]
    p_right = p1
    p_left = p
    while p_right < len(sf_list):
        if isinstance(sf_list[p_right], int):
            sf_list[p_right] += v2
            break
        p_right += 1
    while p_left:
        if isinstance(sf_list[p_left], int):
            sf_list[p_left] += v1
            break
        p_left -= 1

    del (sf_list[p:p1 + 1])
    sf_list.insert(p, 0)


def split(sf_list):
    for p, v in enumerate(sf_list):
        if isinstance(v, int) and v > 9:
            left = math.floor(v / 2)
            right = math.ceil(v / 2)
            new_elements = ["[", left, ",", right, "]"]
            del (sf_list[p])
            sf_list[p:p] = new_elements
            return True
    return False


def reduce(sf_list):
    while True:
        if explode(sf_list):
            continue
        if split(sf_list):
            continue
        break


def run():
    input_data = load_input_data()
    # input_data  = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    lines = [line for line in input_data.split("\n")]
    # lines = grid_from_lines(input_data, transform=int)
    print("solution1 = ", solution1(lines))
    print("solution2 = ", solution2(lines))


def solution1(lines):
    line = make_snailfish_list(lines[0])
    reduce(line)
    for add_line in lines[1:]:
        line = add_sf_lists(add_line, line)
        reduce(line)

    line = sf_list_to_str(line)
    n = make_snailfish_number(line)
    return n.magnitude()


def add_sf_lists(sf_str, line):
    line = sf_list_to_str(line)
    line = "[" + line + "," + sf_str + "]"
    line = make_snailfish_list(line)
    return line


def solution2(lines):
    combos = combinations(lines, 2)
    mags = chain([pair_magnitude(a, b) for a, b in combos],
                 [pair_magnitude(b, a) for a, b in combos])
    return max(mags)


def pair_magnitude(a, b):
    a = make_snailfish_list(a)
    reduce(a)
    sf_list = add_sf_lists(b, a)
    reduce(sf_list)
    n = make_snailfish_number(sf_list_to_str(sf_list))
    mag = n.magnitude()
    return mag


if __name__ == "__main__":
    run()

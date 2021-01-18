from collections import deque, namedtuple
from contextlib import suppress
from enum import Enum

from aocd_tools import load_input_data


class TokenType(Enum):
    OPEN_BRACKET = 0
    CLOSE_BRACKET = 1
    OPERATION = 2
    INT = 3


Token = namedtuple("token", "type value")


def tokenise(line):
    tokens = []
    level = 0
    line = deque(line)
    while line:
        token = line.popleft()
        if not token:
            continue
        if token.startswith("("):
            tokens.append(Token(TokenType.OPEN_BRACKET, level))
            level += 1
            line.appendleft(token[1:])
        elif ")" in token:
            level -= 1
            if level < 0:
                raise ValueError("Unexpected ')'")
            left, _, right = token.partition(")")
            if left:
                tokens.append(Token(TokenType.INT, int(left)))
            line.appendleft(right)
            tokens.append(Token(TokenType.CLOSE_BRACKET, level))
        elif token[:1] in "0123456789":
            try:
                tokens.append(Token(TokenType.INT, int(token)))
            except ValueError:
                print("Invalid int: ", token)
        else:
            ops = {
                "+": op_plus,
                "*": op_mul
            }
            tokens.append(Token(TokenType.OPERATION, ops[token.strip()]))

    return tokens


def evaluate(line):
    tokens = tokenise(line)
    return evaluate_tokens(tokens)


def evaluate_advanced(line):
    tokens = tokenise(line)
    return evaluate_tokens_advanced(tokens)


class NoBrackets(ValueError):
    pass


def find_bracket(tokens):
    for i, t in enumerate(tokens):
        if t.type == TokenType.OPEN_BRACKET:
            level = t.value
            end = tokens.index(Token(TokenType.CLOSE_BRACKET, level))
            return i, end
    raise NoBrackets


def evaluate_tokens_advanced(tokens):
    with suppress(NoBrackets):
        while True:
            start, end = find_bracket(tokens)
            v = evaluate_tokens_advanced(tokens[start + 1:end])
            before = tokens[:start]
            after = tokens[end + 1:]
            tokens = before
            tokens.append(Token(TokenType.INT, v))
            tokens.extend(after)

    while tokens:
        try:
            i_plus = tokens.index(Token(TokenType.OPERATION, op_plus))
            v = evaluate_tokens(tokens[i_plus -1: i_plus + 2])
            before = tokens[:i_plus - 1]
            after = tokens[i_plus + 2:]
            tokens = before
            tokens.append(Token(TokenType.INT, v))
            tokens.extend(after)
        except ValueError:
            return evaluate_tokens(tokens)


def op_plus(a, b):
    return a + b


def op_mul(a, b):
    return a * b


def evaluate_tokens(tokens):
    value = 0
    op = op_plus
    while tokens:
        token = tokens.pop(0)
        if token.type == TokenType.OPEN_BRACKET:
            level = token.value
            end = tokens.index(Token(TokenType.CLOSE_BRACKET, level))
            v = evaluate_tokens(tokens[: end])
            value = op(value, v)
            tokens = tokens[end + 1:]
        elif token.type == TokenType.INT:
            value = op(value, token.value)
        elif token.type == TokenType.OPERATION:
            op = token.value
    return value


def parse(line):
    return line.split(" ")


def run():
    input_data = load_input_data(2020, 18)
    print(f"loaded input data ({len(input_data)} bytes)")
    lines = [parse(line) for line in input_data.split("\n")]
    print("solution1 = ", solution1(lines))
    lines = [parse(line) for line in input_data.split("\n")]
    print("solution2 = ", solution2(lines))


def solution1(lines):
    return sum([evaluate(line) for line in lines])


def solution2(lines):
    return sum([evaluate_advanced(line) for line in lines])


if __name__ == "__main__":
    run()

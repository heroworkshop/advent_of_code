from collections import deque

from aocd_tools import load_input_data

EXAMPLE = """
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""


def parse_crates(lines):
    rows = []
    for line in lines:
        if "[" in line:
            row = [line[x] for x in range(1, len(line), 4)]
            rows.append(row)
    return rows


def make_stack(s):
    return deque([c for c in s if c != " "])


def parse_instruction(instruction):
    words = instruction.split()
    n = int(words[1])
    move_from = int(words[3])
    move_to = int(words[5])
    return n, move_from, move_to


def move_crates(instruction, stacks):
    n, move_from, move_to = parse_instruction(instruction)
    for _ in range(n):
        crate = stacks[move_from - 1].popleft()
        stacks[move_to - 1].appendleft(crate)


def move_crates_multi(instruction, stacks):
    n, move_from, move_to = parse_instruction(instruction)
    buffer = []
    for _ in range(n):
        crate = stacks[move_from - 1].popleft()
        buffer.append(crate)
    for crate in reversed(buffer):
        stacks[move_to - 1].appendleft(crate)


def run(create_mover):
    input_data = load_input_data()
    # input_data  = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")

    crates, instructions = input_data.split("\n\n")

    crates = parse_crates(crates.split("\n"))
    stacks = zip(*crates)
    stacks = [make_stack(s) for s in stacks]

    for instruction in instructions.split("\n"):
        create_mover(instruction, stacks)
        # show(stacks)

    solution = "".join([stack[0] for stack in stacks])
    print("solution = ", solution)


def show(stacks):
    for i, stack in enumerate(stacks):
        print(f"{i + 1}: {stack}")


if __name__ == "__main__":
    run(move_crates)
    run(move_crates_multi)

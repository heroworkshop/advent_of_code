from contextlib import suppress

from aocd_tools import load_input_data
from y2020.vm import GameBoy, parse_lines, Instruction, RepeatedInstruction

EXAMPLE = """
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6""".strip()


def run(input_data):
    print(f"loaded input data ({len(input_data)} bytes)")
    print("solution1 = ", solution1(input_data.split("\n")))
    print("solution2 = ", solution2(input_data.split("\n")))


def solution1(lines):
    program = parse_lines(lines)
    game_boy = GameBoy(program)
    try:
        game_boy.run()
    except RepeatedInstruction as e:
        return e
    return "ERROR!"


def solution2(lines):
    program = parse_lines(lines)
    suspect_lines = [n for n, v in enumerate(program) if v.op in ["jmp", "nop"]]
    print("Found ", len(suspect_lines), " suspect lines")
    for tweek_line in suspect_lines:
        modified_program = parse_lines(lines)
        old = modified_program[tweek_line]
        new_instruction = "nop" if old.op == "jmp" else "jmp"
        modified_program[tweek_line] = Instruction(new_instruction, old.params)
        game_boy = GameBoy(modified_program)
        with suppress(RepeatedInstruction):
            game_boy.run()
            return game_boy.accumulator
    return "ERROR: All tweeks failed"


if __name__ == "__main__":
    run(load_input_data(2020, 8))

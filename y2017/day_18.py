from aocd_tools import load_input_data
from y2017.sound_chip import SoundChip, ConnectedChip

SAMPLE_CODE = """set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2"""


def run():
    input_data = load_input_data(2017, 18)
    print(f"loaded input data ({len(input_data)} bytes)")
    # print(input_data)

    print("solution1 = ", solution1(input_data))
    print("solution2 = ", solution2(input_data))


def solution1(program):
    def on_recover(chip):
        chip.running = False

    #program = SAMPLE_CODE
    chip1 = SoundChip(program, on_recover=on_recover)
    chip1.run()
    return chip1.last_sound


def solution2(program):

    chip1 = ConnectedChip(program)
    chip2 = ConnectedChip(program)
    result = 0
    return result


if __name__ == "__main__":
    run()

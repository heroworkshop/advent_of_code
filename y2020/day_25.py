from aocd_tools import load_input_data


def parse(line):
    return int(line)


EXAMPLE = """
5764801
17807724
""".strip()

def run():
    input_data = load_input_data(2020, 25)
    #input_data= EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    card, door = [parse(line) for line in input_data.split("\n")]
    print("solution1 = ", solution1(card, door))
    print("solution2 = ", solution2(card, door))


def solution1(card, door):

    card_loop = find_loop_size(card)
    door_loop = find_loop_size(door)
    print(f"card loop size = {card_loop}")
    print(f"door loop size = {door_loop}")
    return transform(door, card_loop)


def transform(subject_number, loop_size):
    value = 1
    modulo = 20201227
    for _ in range(loop_size):
        value *= subject_number
        value = value % modulo
    return value

def find_loop_size(public_key):
    subject_number = 7
    value = 1
    loop = 0
    modulo = 20201227
    while value != public_key:
        loop += 1
        value *= subject_number
        value = value % modulo

    return loop


def solution2(lines):
    return


if __name__ == "__main__":
    run()

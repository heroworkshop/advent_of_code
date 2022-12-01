from input_data.day1 import INPUT_DATA


def parse(line):
    return int(line)


def run():
    input_data = [parse(line) for line in INPUT_DATA.split("\n")]
    print("solution1=", solution1(input_data))
    print("solution2=", solution2(input_data))


def solution1(input_data):
    return


def solution2(input_data):
    return


if __name__ == "__main__":
    run()

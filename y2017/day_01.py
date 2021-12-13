from aocd_tools import load_input_data


def run():
    input_data = load_input_data(2017, 1)
    print(f"loaded input data ({len(input_data)} bytes)")

    print("solution1 = ", solution1(input_data))
    print("solution2 = ", solution2(input_data))


def solution1(digits):
    digits = list(digits)
    digits.append(digits[0])
    checksum = sum([
        int(a) for a, b in zip(digits[:-1], digits[1:])
        if a == b
    ])
    return checksum


def solution2(digits):
    digits = list(digits)
    offset = len(digits) // 2
    digits.extend(digits)
    checksum = sum([
        int(a) for a, b in zip(digits[:offset * 2], digits[offset:])
        if a == b
    ])
    return checksum


if __name__ == "__main__":
    run()

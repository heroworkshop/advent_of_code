from hashlib import md5

from aocd_tools import load_input_data


def run():
    input_data = load_input_data(2015, 4)
    print(f"loaded input data ({len(input_data)} bytes)")
    print("solution1 = ", solution1(input_data))
    print("solution2 = ", solution2(input_data))


def solution1(secret):
    suffix = 0
    while True:
        v = md5(f"{secret}{suffix}".encode('utf-8')).hexdigest()
        if v[:5] == "00000":
            return suffix
        suffix += 1

def solution2(secret):
    suffix = 0
    while True:
        v = md5(f"{secret}{suffix}".encode('utf-8')).hexdigest()
        if v[:6] == "000000":
            return suffix
        suffix += 1


if __name__ == "__main__":
    run()

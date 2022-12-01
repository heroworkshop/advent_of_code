from _md5 import md5
from contextlib import suppress

from input_data.day1 import INPUT_DATA


def parse(line):
    return int(line)


def run():
    door_id = "ffykfhsq"

    print("solution1=", solution1(door_id))
    print("solution2=", solution2(door_id))


def solution1(door_id):
    index = 0
    result = []
    while len(result) < 8:
        key = f"{door_id}{index}".encode()
        hash_result = md5(key).digest().hex()

        if hash_result.startswith("00000"):
            result.append(hash_result[5])
        index += 1
    return "".join(result)


def solution2(door_id):
    index = 0
    result = list("--------")
    while "-" in result:
        key = f"{door_id}{index}".encode()
        hash_result = md5(key).digest().hex()

        if hash_result.startswith("00000"):
            with suppress(ValueError):
                pos = int(hash_result[5])
                if pos < 8 and result[pos] == "-":
                    result[pos] = hash_result[6]
                    print("".join(result))
        index += 1
    return "".join(result)



if __name__ == "__main__":
    run()

from aocd_tools import load_input_data


def run():
    input_data = load_input_data(2015, 5)
    print(f"loaded input data ({len(input_data)} bytes)")
    lines = input_data.split("\n")
    print("solution1 = ", solution1(lines))
    print("solution2 = ", solution2(lines))


def contains_double(string):
    last = None
    for x in string:
        if x == last:
            return True
        last = x
    return False


def is_nice(string):
    vowels = [x for x in string if x in "aeiou"]
    if len(vowels) < 3:
        return False
    if not contains_double(string):
        return False
    for bad in ["ab", "cd", "pq", "xy"]:
        if bad in string:
            return False
    return True


def contains_repeating_pair(string):
    last = string[0]
    p = 2
    for x in string[1:]:
        pair = last + x
        if pair in string[p:]:
            return True
        last = x
        p += 1
    print("No repeating pair")
    return False


def contains_split_pair(string):
    p = 2
    while p < len(string):
        if string[p] == string[p - 2]:
            return True
        p += 1
    print("No split pair")
    return False


def is_new_nice(string):
    print(string)
    return contains_repeating_pair(string) and contains_split_pair(string)


def solution1(lines):
    nice_strings = [line for line in lines if is_nice(line)]
    return len(nice_strings)


def solution2(lines):
    nice_strings = [line for line in lines if is_new_nice(line)]
    return len(nice_strings)


if __name__ == "__main__":
    run()

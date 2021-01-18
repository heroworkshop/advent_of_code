from aocd_tools import load_input_data


def run():
    input_data = load_input_data(2017, 4)
    print(f"loaded input data ({len(input_data)} bytes)")
    pass_phrases = [x.split() for x in input_data.split("\n")]
    print("solution1 = ", solution1(pass_phrases))
    print("solution2 = ", solution2(pass_phrases))


def solution1(pass_phrases):
    valid_phrases = [phrase for phrase in pass_phrases if is_valid(phrase)]
    return len(valid_phrases)


def is_valid(phrase):
    return len(phrase) == len(set(phrase))


def is_valid_advanced(phrase):
    sorted_phrase = [tuple(sorted(p)) for p in phrase]
    return len(sorted_phrase) == len(set(sorted_phrase))


def solution2(pass_phrases):
    valid_phrases = [phrase for phrase in pass_phrases if is_valid_advanced(phrase)]
    return len(valid_phrases)


if __name__ == "__main__":
    run()

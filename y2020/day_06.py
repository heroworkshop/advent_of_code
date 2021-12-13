from aocd_tools import load_input_data

EXAMPLE = """
abc

a
b
c

ab
ac

a
a
a
a

b""".strip()

def run():
    input_data = load_input_data(2020, 6)
    print(f"loaded input data ({len(input_data)} bytes)")
    print("solution1 = ", solution1(input_data.split("\n\n")))
    print("solution2 = ", solution2(input_data.split("\n\n")))


def count_unique(group):
    answers = {answer for answer in group if answer.strip()}
    return len(answers)


def count_common(group):
    people = group.split("\n")
    answers = []
    for p in people:
        answers.append({a for a in p})

    print(answers)

    common = answers[0]
    for a in answers[1:]:
        common = common.intersection(a)

    return len(common)


def solution1(groups):
    counts = [count_unique(group) for group in groups]

    return sum(counts)


def solution2(groups):
    counts = [count_common(group) for group in groups]

    return sum(counts)


if __name__ == "__main__":
    run()

from aocd_tools import load_input_data

EXAMPLE = """A Y
B X
C Z"""


def run():
    input_data = load_input_data(2022, 2)
    # input_data = EXAMPLE

    print(f"loaded input data ({len(input_data)} bytes)")

    entries = input_data.split("\n")
    entries = [e.split() for e in entries]
    print(entries[:50])

    print("solution1 = ", solution1(entries))
    print("solution2 = ", solution2(entries))


def win(a, b):
    winning_moves = {
        (1, 2),
        (2, 3),
        (3, 1)
    }
    print(f"{a} {b}", end=" ")
    if (a, b) in winning_moves:
        print("win", end="")
        return 6
    if a == b:
        print("draw", end="")
        return 3
    print("loss", end="")
    return 0


def solution1(entries):
    abc_map = {"A": 1, "B": 2, "C": 3}
    xyz_map = {"X": 1, "Y": 2, "Z": 3}
    scores = []
    for a, b in entries:
        print(a, b, end=" ")
        opponent = abc_map[a]
        myself = xyz_map[b]
        score = win(opponent, myself) + myself
        print(" -> ", score)
        scores.append(score)

    return sum(scores)


def play_from_result(a, result):
    if result == "draw":
        return a
    b_map = {1: 2, 2: 3, 3: 1} if result == "win" else {1: 3, 2: 1, 3: 2}
    return b_map[a]


def solution2(entries):
    abc_map = {"A": 1, "B": 2, "C": 3}
    xyz_map = {"X": "lose", "Y": "draw", "Z": "win"}
    scores = []
    for a, b in entries:
        print(a, b, end=" ")
        opponent = abc_map[a]
        result = xyz_map[b]
        myself = play_from_result(opponent, result)
        score = win(opponent, myself) + myself
        print(" -> ", score)
        scores.append(score)

    return sum(scores)


if __name__ == "__main__":
    run()

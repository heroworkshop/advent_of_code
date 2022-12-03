from collections import defaultdict
from functools import lru_cache
from pprint import pprint

from aocd_tools import load_input_data, Grid

EXAMPLE = """"""


def parse(line):
    return line


def run():
    print("solution1 = ", solution1(2, 5))
    print("solution2 = ", solution2(2, 5))


def deterministic_dice():
    n = 1
    while True:
        yield n
        n += 1
        if n > 100:
            n = 1


def solution1(p1, p2):
    dice = deterministic_dice()
    positions = [p1 - 1, p2 - 1]
    scores = [0, 0]
    turn = 0
    die_rolls = 0
    while all(s < 1000 for s in scores):
        dice_roll = next(dice) + next(dice) + next(dice)
        die_rolls += 3
        positions[turn] += dice_roll
        score = 1 + positions[turn] % 10
        scores[turn] += score
        print(f"player {turn + 1} rolls {dice_roll} and moves to {score} for a total score of {scores[turn]}")
        turn = (turn + 1) % 2

    return min(scores) * die_rolls


def make_defaultdict_int():
    return defaultdict(int)


roll_distribution = defaultdict(int)
for r1 in range(1, 4):
    for r2 in range(1, 4):
        for r3 in range(1, 4):
            roll_distribution[sum((r1, r2, r3))] += 1


@lru_cache(maxsize=None)
def count_wins(score1, score2, pos1, pos2):
    if score1 >= 21: return 1, 0
    if score2 >= 21: return 0, 1
    win1, win2 = 0, 0
    for roll, count in roll_distribution.items():
        new_pos = 1 + (pos1 + roll - 1) % 10
        new_score = score1 + new_pos
        add_win2, add_win1 = count_wins(score2, new_score, pos2, new_pos)
        win1 += add_win1 * count
        win2 += add_win2 * count
    return win1, win2


def solution2(pos1, pos2):
    return count_wins(0, 0, pos1, pos2)


def solution2_aargh(p1, p2):
    roll_distribution = defaultdict(int)
    for r1 in range(1, 4):
        for r2 in range(1, 4):
            for r3 in range(1, 4):
                roll_distribution[sum((r1, r2, r3))] += 1

    pprint(roll_distribution)

    positions = defaultdict(make_defaultdict_int)
    positions[(p1, p2)][(0, 0)] += 1
    wins1 = wins2 = 0

    while positions:
        new_positions = defaultdict(make_defaultdict_int)
        for roll1, count1 in roll_distribution.items():
            for roll2, count2 in roll_distribution.items():
                multiplier = count2 * count1
                for p, scores in positions.items():
                    p1, p2 = p
                    p1 = 1 + (p1 + roll1 - 1) % 10
                    p2 = 1 + (p2 + roll2 - 1) % 10
                    for s, count in scores.items():
                        s1, s2 = s
                        s1 += p1
                        s2 += p2
                        new_count = count * multiplier
                        if s1 >= 21:
                            wins1 += new_count
                        elif s2 >= 21:
                            wins2 += new_count
                        else:
                            new_positions[(p1, p2)][(s1, s2)] = new_count
        positions = new_positions
        print(wins1, wins2)

    return max((wins1, wins2))


if __name__ == "__main__":
    run()

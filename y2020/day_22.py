from collections import deque
from copy import deepcopy

from aocd_tools import load_input_data


EXAMPLE = """
Player 1: 
9
2
6
3
1

Player 2:
5
8
4
7
10
""".strip()

def parse(player):
    return deque([int(line) for line in player.split("\n")[1:]])


def run():
    input_data = load_input_data(2020, 22)
    # input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    decks = ([parse(player) for player in input_data.split("\n\n")])
    print(decks)
    print("solution1 = ", solution1(deepcopy(decks)))
    print("solution2 = ", solution2(decks))


def solution1(decks):
    while all(decks):
        cards = [deck.popleft() for deck in decks]
        if cards[0] > cards[1]:
            decks[0].extend(cards)
        else:
            decks[1].extend(reversed(cards))

    scores = [calculate_score(deck) for deck in decks]
    return sum(scores)


def calculate_score(deck):
    scores = [i * card for i, card in enumerate(reversed(deck), 1)]
    return sum(scores)


def solution2(decks):
    decks = recursive_combat(decks)
    scores = [calculate_score(deck) for deck in decks]
    return sum(scores)

game = 0
def recursive_combat(decks):
    global game
    game += 1
    print(f"Game {game} ", end="", flush=True)
    round = 0
    previous_hands = set()
    while all(decks):
        round += 1

        signature = (tuple(decks[0]), tuple(decks[1]))
        if signature in previous_hands:
            return [decks[0], deque([])]
        previous_hands.add(signature)

        cards = [deck.popleft() for deck in decks]

        if cards[0] <= len(decks[0]) and cards[1] <= len(decks[1]):
            results = recursive_combat(new_decks(decks, cards))
            verdict = [len(r) for r in results]
        else:
            verdict = cards
        if verdict[0] > verdict[1]:
            decks[0].extend(cards)
        else:
            decks[1].extend(reversed(cards))
        if round > 1000000:
            print(f"r{round }")

        if round > 1000010:
            raise RuntimeError("Got stuck in infinite loop")

    print(f"r{round}")
    return decks


def new_decks(decks, counts):
    print(f"making new decks ({counts}) from:\n {decks}")
    result = [deque(list(d)[:c]) for d, c in zip(decks, counts)]
    print(f" -> {result}")
    return result


if __name__ == "__main__":
    run()

from collections import namedtuple, defaultdict
from contextlib import suppress

from input_data.day10 import INPUT_DATA

GiveTo = namedtuple("give_to", "high low")


class Robot:
    def __init__(self, id_tag, trackers=None):
        self.id_tag = id_tag
        self.chips = []
        self.give_to = None
        self.trackers = trackers or []

    def take(self, chip):
        self.chips.append(chip)
        self.on_update()

    def on_update(self):
        if len(self.chips) == 2:
            # print(f"Bot-{self.id_tag} giving to {self.give_to}")
            if self.give_to:
                self.give()

    def add_give_rule(self, rule: GiveTo):
        self.give_to = rule
        self.on_update()

    def give(self):
        assert self.give_to
        self.chips.sort()
        for t in self.trackers:
            t.on_compare(self)
        low = self.chips.pop(0)
        high = self.chips.pop(0)
        self.give_to.low.take(low)
        self.give_to.high.take(high)

    def __repr__(self):
        return f"Bot-{self.id_tag}"


class Output:
    def __init__(self, id_tag, trackers=None):
        self.id_tag = id_tag
        self.chips = set()
        self.trackers = trackers or []

    def take(self, chip):
        self.chips.add(chip)

    def __repr__(self):
        return f"Output-{self.id_tag}"


def run():
    input_data = INPUT_DATA.split("\n")
    print("solution1=", solution1(input_data))
    print("solution2=", solution2(input_data))


class Tracker:
    def __init__(self, chips):
        self.chips = chips
        self.matches = set()

    def on_compare(self, robot):
        print(f"{robot.id_tag} is comparing {robot.chips}")
        if all(c in robot.chips for c in self.chips):
            self.matches.add(robot.id_tag)


def solution1(input_data):
    takers = dict()
    tracker = Tracker(["61", "17"])
    for line in input_data:
        parts = line.split(" ")
        target_id = parts[-1]
        if "goes" in line:
            chip = parts[1]
            destination = make_taker("bot", target_id, takers, tracker)
            print(f"Giving {chip} to {target_id}")
            destination.take(chip)
        elif "gives" in line:
            bot_id = parts[1]
            low_type = parts[5]
            high_type = parts[10]
            low_id = parts[6]
            high_id = parts[11]
            low = make_taker(low_type, low_id, takers, tracker)
            high = make_taker(high_type, high_id, takers, tracker)
            bot = make_taker("bot", bot_id, takers, tracker)
            print(f"{bot_id}: add rule high {high_type}{high_id} low {low_type}{low_id}")
            bot.add_give_rule(GiveTo(high, low))

    return tracker.matches


def make_taker(type_name, taker_id, takers, tracker):
    type_names = {"output": Output, "bot": Robot}
    key = f"{type_name} {taker_id}"

    if key not in takers:
        takers[key] = type_names[type_name](taker_id, [tracker])

    return takers[key]


def solution2(input_data):
    return


if __name__ == "__main__":
    run()

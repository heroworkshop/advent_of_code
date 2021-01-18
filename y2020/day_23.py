from aocd_tools import load_input_data


def parse(line):
    return int(line)


def run():
    input_data = "253149867"
    print(f"loaded input data ({len(input_data)} bytes)")
    line = [int(ch) for ch in input_data]
    s1 = solution1(line)
    line = [int(ch) for ch in input_data]
    s2 = solution2(line)
    print("solution1 = ", s1)
    print("solution2 = ", s2)
    assert s1 == s2


def solution1(line):
    length = len(line)
    current = 0
    for move in range(100):
        print(f"--- move {move + 1} ---")
        current_val = line[current]
        print("cups: ", render_line(line, current_val))
        pick_up = pick_up_from(line, current + 1)
        print("pick up: ", pick_up)

        destination = current_val - 1
        while destination not in line:
            destination -= 1
            if destination < 1:
                destination = 9
        print(f"destination: {destination}")
        dest_p = line.index(destination) + 1
        while pick_up:
            line.insert(dest_p, pick_up.pop())
            # print(render_line(line, current_val))
        current = (line.index(current_val) + 1) % length

    answer = line[line.index(1) + 1:]
    answer.extend(line[:line.index(1)])
    return "".join([str(i) for i in answer])


def pick_up_from(line, p):
    pick_up = []
    while len(pick_up) < 3:
        if p >= len(line):
            p = 0
        pick_up.append(line.pop(p))
    return pick_up


def pick_up_from_dict(cups, positions, p):
    pick_up = []
    while len(pick_up) < 3:
        try:
            cup_v = cups[p]
            cups[p] = None
            positions[cup_v] = None
            p += 1
            pick_up.append(cup_v)
        except IndexError:
            p = 0

    return pick_up


def render_line(line, current_val):
    result = [f"({v})" if v == current_val else f"{v}" for v in line]
    return " ".join(result)


def solution2(line):
    length = len(line)
    cups = {i: cup for i, cup in enumerate(line)}
    positions = {cup: i for i, cup in cups.items()}
    current = 0
    max_v = 9
    for move in range(100):
        print(f"--- move {move + 1} ---")
        current_val = cups[current]
        print("cups: ", render_line(line, current_val))
        pick_up = pick_up_from_dict(cups, positions, current + 1)
        print("pick up: ", pick_up)

        destination = current_val - 1
        while positions[destination] is None:
            destination -= 1
            if destination < 1:
                destination = max_v
        print(f"destination: {destination}")
        dest_p = positions[destination] + 1
        while pick_up:

            line.insert(dest_p, pick_up.pop())

        current = (line.index(current_val) + 1) % length

    answer = line[line.index(1) + 1:]
    answer.extend(line[:line.index(1)])
    return "".join([str(i) for i in answer])


if __name__ == "__main__":
    run()

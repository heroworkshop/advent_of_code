from aocd_tools import load_input_data, ints_from_lines

EXAMPLE = """
0
3
0
1
-3""".strip()

def run():
    input_data = load_input_data(2017, 5)
    # input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    maze = ints_from_lines(input_data)
    print("solution1 = ", solution1(maze))
    maze = ints_from_lines(input_data)
    print("solution2 = ", solution2(maze))


def solution1(maze):
    p = 0
    step = 0
    try:
        while True:
            jmp = maze[p]
            maze[p] += 1
            p += jmp
            step += 1
    except IndexError:
        pass
    return step


def solution2(maze):
    p = 0
    step = 0
    try:
        while True:
            jmp = maze[p]
            maze[p] += 1 if jmp < 3 else -1
            p += jmp
            step += 1
    except IndexError:
        pass
    return step


if __name__ == "__main__":
    run()

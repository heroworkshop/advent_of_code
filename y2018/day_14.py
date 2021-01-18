from aocd_tools import load_input_data, ints_from_lines


def new_recipes(a, b):
    s = a + b
    result = "{}".format(s)
    return [int(v) for v in result]


def solve1(offset):
    offset = int(offset)
    recipes = [3, 7]
    elf1 = 0
    elf2 = 1
    while len(recipes) < offset + 10:
        recipes.extend(new_recipes(recipes[elf1], recipes[elf2]))
        # print(recipes)
        elf1 = (elf1 + 1 + recipes[elf1]) % len(recipes)
        elf2 = (elf2 + 1 + recipes[elf2]) % len(recipes)
    print("solution 1")
    for i in range(offset, offset + 10):
        print(recipes[i], end="")
    print()


def solve2(offset):
    target = [int(v) for v in offset]
    print("Looking for ", target)

    recipes = [3, 7]
    elf1 = 0
    elf2 = 1
    tail_length = len(target)

    while True:
        recipes.extend(new_recipes(recipes[elf1], recipes[elf2]))
        elf1 = (elf1 + 1 + recipes[elf1]) % len(recipes)
        elf2 = (elf2 + 1 + recipes[elf2]) % len(recipes)
        # print(recipes[-tail_length:])
        if target == recipes[-tail_length:]:
            break
    print("solution 2: ", len(recipes) - tail_length)


def run():
    input_data = load_input_data(2018, 14)
    print(f"loaded input data ({len(input_data)} bytes)")
    offset = input_data
    print(offset)
    #solve1(offset)
    solve2(offset)


if __name__ == "__main__":
    run()

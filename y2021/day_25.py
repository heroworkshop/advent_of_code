from collections import defaultdict, namedtuple


from aocd_tools import load_input_data, grid_from_lines

EXAMPLE = """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>"""

EXAMPLE2="""...>...
.......
......>
v.....>
......>
.......
..vvv.."""


def extract_positions(grid, ch):
    return {(x, y)
            for x in range(grid.width)
            for y in range(grid.height)
            if grid.at((x, y)) == ch}


def run():
    input_data = load_input_data()
    #input_data  = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    # lines = [parse(line) for line in input_data.split("\n")]
    grid = grid_from_lines(input_data, transform=str)

    east_movers = extract_positions(grid, ">")
    south_movers = extract_positions(grid, "v")
    print("solution1 = ", solution1(grid, east_movers, south_movers))
    print("solution2 = ", solution2(grid, east_movers, south_movers))


def solution1(grid, east_movers, south_movers):
    print(grid.render())
    width, height = grid.width, grid.height
    step = 0
    while True:
        count = 0
        step += 1
        movers = dict()
        for p in east_movers:
            x, y = p
            x = (x + 1) % width
            if (x, y) not in east_movers and (x, y) not in south_movers:
                movers[p] = (x, y)
        for p1, p2 in movers.items():
            east_movers.remove(p1)
            grid.add(p1, ".")
            east_movers.add(p2)
            grid.add(p2, ">")
            count += 1

        movers = dict()
        for p in south_movers:
            x, y = p
            y = (y + 1) % height
            if (x, y) not in east_movers and (x, y) not in south_movers:
                movers[p] = (x, y)
        for p1, p2 in movers.items():
            south_movers.remove(p1)
            grid.add(p1, ".")
            south_movers.add(p2)
            grid.add(p2, "v")
            count += 1
        print("Step", step)
        #print(grid.render())
        if count == 0:
            break

    return step


def solution2(grid, east_movers, south_movers):
    return None


if __name__ == "__main__":
    run()

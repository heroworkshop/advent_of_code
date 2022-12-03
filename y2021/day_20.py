from collections import defaultdict, namedtuple


from aocd_tools import load_input_data, Grid, grid_from_lines

EXAMPLE = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###"""


def parse(parts):
    pixel = {"#": "1", ".": "0"}
    algorithm = [pixel[ch] for ch in parts[0]]

    input_image = grid_from_lines(parts[1], default_val="0", transform=lambda x: pixel[x])
    return algorithm, input_image


def run():
    input_data = load_input_data()
    # input_data  = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    algorithm, input_image = parse(input_data.split("\n\n"))
    # lines = grid_from_lines(input_data, transform=int)
    print("solution1 = ", solution1(algorithm, input_image))
    print("solution2 = ", solution2(algorithm, input_image))


def solution1(algorithm, input_image):
    print(input_image.render(render_char=lambda x: "#" if x == "1" else "."))

    for _ in range(2):
        input_image = enhance_image(algorithm, input_image)
        print(input_image.render(render_char=lambda x: "#" if x == "1" else "."))

    return sum(int(ch) for ch in input_image.grid.values())


def solution2(algorithm, input_image):

    for _ in range(50):
        input_image = enhance_image(algorithm, input_image)

    return sum(int(ch) for ch in input_image.grid.values())


def enhance_image(algorithm, input_image):
    new_default = algorithm[0] if input_image.default_val == "0" else algorithm[511]
    image = Grid(default_val=new_default)
    input_image.update_bounds()
    for x in range(input_image.x_bounds.min - 1, input_image.x_bounds.max + 2):
        for y in range(input_image.y_bounds.min - 1, input_image.y_bounds.max + 2):
            binval = [input_image.at(p) for p in input_image.rect((x, y))]
            binval = "".join(binval)
            index = int(binval, 2)
            pixel = algorithm[index]
            image.add((x, y), pixel)

    return image

if __name__ == "__main__":
    run()

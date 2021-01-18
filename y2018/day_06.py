from collections import namedtuple, defaultdict

from aocd_tools import load_input_data, int_tuples_from_lines

EXAMPLE = """1, 1
    1, 6
    8, 3
    3, 4
    5, 5
    8, 9"""

TEST1 = """1, 1
    1, 6
    4, 4
    6, 7
    8, 3
    3, 4
    5, 5"""

def get_bounds(values):
    Boundary = namedtuple("boundary", "min max")
    return Boundary(min(values) - 1, max(values) + 1)


def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


class cell:
    def __init__(self):
        self.nearest_node = None
        self.distance = 1000000000


class Grid:
    def __init__(self, bounds):
        self.x_bounds, self.y_bounds = bounds
        self.grid = defaultdict(cell)

    def update(self, node_id, position):
        for x in range(self.x_bounds.min, self.x_bounds.max + 1):
            for y in range(self.y_bounds.min, self.y_bounds.max + 1):
                current = self.grid[(x, y)]
                distance = manhattan_distance(position, (x, y))
                if distance == current.distance:
                    current.nearest_node = -1
                    self.grid[(x, y)] = current
                elif distance < current.distance:
                    current.distance = distance
                    current.nearest_node = node_id

    def area(self, node_id, position):
        queue = [position]
        done = set()
        count = 0
        while queue:
            p = queue.pop(0)
            if p in done:
                continue

            x, y = p
            if x < self.x_bounds.min or x > self.x_bounds.max:
                return 0
            if y < self.y_bounds.min or y > self.y_bounds.max:
                return 0

            done.add(p)
            if node_id == self.grid[p].nearest_node:
                count += 1
                queue.append((x + 1, y))
                queue.append((x - 1, y))
                queue.append((x, y + 1))
                queue.append((x, y - 1))
        return count

    def render(self, file):
        for y in range(self.y_bounds.min, self.y_bounds.max + 1):
            for x in range(self.x_bounds.min, self.x_bounds.max + 1):
                ch = make_ch(self.grid[(x, y)].nearest_node)
                print(ch, file=file, end="")
            print(file=file)


def make_ch(i):
    return chr(ord("A") + i)

def run():
    input_data = TEST1
    input_data = load_input_data(2018, 6)
    print(f"loaded input data ({len(input_data)} bytes)")

    coords = int_tuples_from_lines(input_data, ",")
    x_bounds = get_bounds([c[0] for c in coords])
    y_bounds = get_bounds([c[1] for c in coords])
    print(x_bounds)
    print(y_bounds)

    grid = Grid((x_bounds, y_bounds))

    print("Plotting...", end="")
    for node_id, coord in enumerate(coords):
        grid.update(node_id, coord)
        print(".", end="", flush=True)
    print()

    with open("grid.txt", "w") as f:
        grid.render(f)

    print("Finding largest area...")
    areas = {grid.area(node_id, coord): node_id for node_id, coord in enumerate(coords)}
    print(areas)

    largest = max(areas)

    print("Answer 1 = ", largest)
    print("node_id = {} ({})".format(areas[largest], make_ch(areas[largest])))

    count = 0
    for x in range(x_bounds.min, x_bounds.max + 1):
        for y in range(y_bounds.min, y_bounds.max + 1):
            distances = [manhattan_distance((x, y), p) for p in coords]
            if sum(distances) < 10000:
                count += 1
    print("Answer 2 = ", count)

if __name__ == "__main__":
    run()

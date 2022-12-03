from collections import defaultdict, namedtuple

from aocd_tools import load_input_data

EXAMPLE = """"""

Vrange = namedtuple("vrange", "lower upper")
XYZ = namedtuple("xyz", "x y z")


class Cuboid:
    def __init__(self, lower, upper):
        self.lower = XYZ(*lower)
        self.upper = XYZ(*upper)

    def __hash__(self):
        return tuple((*self.lower, *self.upper)).__hash__()

    @property
    def volume(self):
        w = self.upper.x - self.lower.x
        h = self.upper.y - self.lower.y
        d = self.upper.z - self.lower.z
        return w * h * d

    def point_is_inside(self, point):
        p = XYZ(*point)
        return (self.lower.x <= p.x <= self.upper.x
                and self.lower.y <= p.y <= self.upper.y
                and self.lower.z <= p.z <= self.upper.z)

    def overlaps(self, cuboid):
        for lo1, hi1, lo2, hi2 in zip(self.lower, self.upper, cuboid.lower, cuboid.upper):
            if lo1 < hi1 < lo2 or hi1 > lo1 > hi2:
                return False
        return True

    def corners(self):
        a = self.lower
        b = self.upper
        return {
            (a.x, a.y, a.z),
            (b.x, a.y, a.z),
            (a.x, b.y, a.z),
            (b.x, b.y, a.z),
            (a.x, a.y, b.z),
            (b.x, a.y, b.z),
            (a.x, b.y, b.z),
            (b.x, b.y, b.z),
        }

    def count_overlaps(self, cuboid):
        """How many of cube's corners are inside self?"""
        corners_inside = [self.point_is_inside(c) for c in cuboid.corners()]
        return sum(corners_inside)

    # def subtract(self, cuboid):
    #     xvals = sorted([self.lower.x, self.upper.x, cuboid.lower.x, cuboid.upper.x])
    #     yvals = sorted([self.lower.y, self.upper.y, cuboid.lower.y, cuboid.upper.y])
    #     zvals = sorted([self.lower.z, self.upper.z, cuboid.lower.z, cuboid.upper.z])
    #     results = set()
    #
    #     x_pairs = [(x1, x2) for x1, x2 in zip(xvals[:-1], xvals[1:]) if x1 != x2]
    #     y_pairs = [(y1, y2) for y1, y2 in zip(yvals[:-1], yvals[1:]) if y1 != y2]
    #     z_pairs = [(z1, z2) for z1, z2 in zip(zvals[:-1], zvals[1:]) if z1 != z2]
    #     for x1, x2 in x_pairs:
    #         for y1, y2 in y_pairs:
    #             for z1, z2 in z_pairs:
    #                 new_cuboid = Cuboid((x1, y1, z1), (x2, y2, z2))
    #                 if (self.count_overlaps(new_cuboid) == 8
    #                         and cuboid.count_overlaps(new_cuboid) != 8):
    #                     results.add(new_cuboid)
    #
    #     return results

    def subtract(self, cuboid):
        bottom_slice = Cuboid(
            (self.lower.x, self.lower.y, self.lower.z),
            (self.upper.x, self.upper.y, max(self.lower.z, cuboid.lower.z))
        )

        top_slice = Cuboid(
            (self.lower.x, self.lower.y, min(cuboid.upper.z, self.upper.z)),
            (self.upper.x, self.upper.y, self.upper.z)
        )

        left_slice = Cuboid(
            (self.lower.x, self.lower.y, bottom_slice.upper.z),
            (max(self.lower.x, cuboid.lower.x), self.upper.y, top_slice.lower.z)
        )

        right_slice = Cuboid(
            (min(cuboid.upper.x, self.upper.x), self.lower.y, top_slice.lower.z),
            (self.upper.x, self.upper.y, top_slice.lower.z)
        )

        front_slice = Cuboid(
            (left_slice.upper.x, self.lower.y, bottom_slice.upper.z),
            (right_slice.lower.x, max(cuboid.lower.y, self.lower.y), top_slice.lower.z)
        )

        back_slice = Cuboid(
            (left_slice.upper.x, min(cuboid.upper.y, self.upper.y), bottom_slice.upper.z),
            (right_slice.lower.x, self.upper.y, top_slice.lower.z)
        )
        all_slices = (bottom_slice, top_slice, left_slice, right_slice, front_slice, back_slice)
        return [c for c in all_slices if c.volume]


def parse(line):
    def split_vrange(v):
        _, vrange = v.split("=")
        t = tuple(int(n) for n in vrange.split(".."))
        return t  # Vrange(t)

    on_off, values = line.split(" ")
    on_off = on_off == "on"

    values = tuple(split_vrange(v) for v in values.split(","))
    return on_off, values


def run():
    input_data = load_input_data()
    # input_data  = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    lines = [parse(line) for line in input_data.split("\n")]
    lines1 = [(turn_on, vrange) for turn_on, vrange in lines
              if -51 < vrange[0][0] < 51 and -51 < vrange[0][1] < 51
              ]
    # lines = grid_from_lines(input_data, transform=int)
    print("solution1 = ", solution1(lines1))
    print("solution2 = ", solution2(lines1))


def solution1(lines):
    on_vals = set()
    for on_off, vrange in lines:
        if not -51 < vrange[0][0] < 51 or not -51 < vrange[0][1] < 51:
            print(f"ignoring {vrange}")
            continue
        print(f"Applying {vrange}")
        values = set(
            (x, y, z)
            for x in range(vrange[0][0], vrange[0][1] + 1)
            for y in range(vrange[1][0], vrange[1][1] + 1)
            for z in range(vrange[2][0], vrange[2][1] + 1)
        )
        if on_off:
            on_vals |= values
        else:
            on_vals -= values
    return len(on_vals)


def solution2(lines):
    cuboids = set()
    for turn_on, vrange in lines:
        new_cuboid = Cuboid((vrange[0][0], vrange[1][0], vrange[2][0]),
                            (vrange[0][1] + 1, vrange[1][1] + 1, vrange[2][1] + 1))
        print("adding" if turn_on else "subtracting", end="")
        print(f" cuboid {new_cuboid.lower} {new_cuboid.upper}")
        overlapping_cuboids = {c for c in cuboids if c.overlaps(new_cuboid)}

        if turn_on:
            new_cuboids = {new_cuboid}
            for cuboid in overlapping_cuboids:
                cubelets = set()
                for new_cuboid in new_cuboids:
                    cubelets.update(new_cuboid.subtract(cuboid))
                new_cuboids = cubelets
            cuboids.update(new_cuboids)
        else:
            cubelets = set()
            for cuboid in cuboids:
                cubelets.update(cuboid.subtract(new_cuboid))
            cuboids = cubelets
    return sum((c.volume for c in cuboids))


if __name__ == "__main__":
    run()

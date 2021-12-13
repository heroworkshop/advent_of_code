from collections import namedtuple
from pprint import pprint

Circle = namedtuple("circle", "x y r")


def overlaps(c1, c2):
    d_squared = (c1.x - c2.x) ** 2 + (c1.y - c2.y) ** 2
    return d_squared <= (c1.r + c2.r) ** 2


class Circles:
    def __init__(self, circles):
        self.circles = [Circle(*c) for c in circles]

    def find_first_overlap(self, circle, group):
        for cn in group:
            if overlaps(self.circles[cn], circle):
                return cn
        return None

    def find_largest_group(self):
        groups = []
        for n, circle in enumerate(self.circles):
            # print(n, circle)
            overlap_group = {n}
            for group in groups:
                overlap = self.find_first_overlap(circle, group)
                if overlap is not None:
                    # print(n, "overlaps ", overlap)
                    overlap_group = overlap_group.union(group)
            groups = [g for g in groups if not g.intersection(overlap_group)]
            groups.append(overlap_group)
            # pprint(groups, indent=4)

        return max(groups, key=len)

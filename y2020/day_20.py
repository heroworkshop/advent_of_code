import math
from collections import namedtuple, defaultdict
from copy import copy
from enum import Enum
from functools import reduce
from typing import List

from aocd_tools import load_input_data, grid_from_lines
from y2020.day_20_example import EXAMPLE

Tile = namedtuple("tile", "id grid edges")
RotatedTile = namedtuple("rotatedtile", "tile rotation")


class Side(Enum):
    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3


def int_from_edgechars(edgechars):
    return int("".join(edgechars).replace(".", "0").replace("#", "1"), 2)


def r(x):
    return list(reversed(x))


def flip(sides):
    top, right, bottom, left = sides
    return bottom, r(right), top, r(left)


def make_edges(grid):
    top = [grid[(x, 0)] for x in range(10)]
    right = [grid[(9, y)] for y in range(10)]
    bottom = [grid[(x, 9)] for x in range(10)]
    left = [grid[(0, y)] for y in range(10)]

    rotations = [
        (top, right, bottom, left),
        (r(left), top, r(right), bottom),
        (r(bottom), r(left), r(top), r(right)),
        (right, r(bottom), left, r(top))
    ]
    flipped = [flip(sides) for sides in rotations]

    rotations.extend(flipped)

    edges = [tuple([int_from_edgechars(e) for e in rotation]) for rotation in rotations]

    return edges


def parse(tile):
    id_line, _, grid_lines = tile.partition("\n")
    tile_id = int(id_line.partition(" ")[-1].partition(":")[0])
    grid = grid_from_lines(grid_lines)
    return Tile(tile_id, grid, make_edges(grid.grid))


def run():
    input_data = load_input_data(2020, 20)
    #input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    tiles = [parse(tile) for tile in input_data.split("\n\n")]
    print(f"found {len(tiles)} tiles")
    print("solution1 = ", solution1(tiles))
    print("solution2 = ", solution2(tiles))


def make_edge_table(tiles):
    table = defaultdict(list)
    for tile in tiles:
        for rotation in tile.edges:
            for edge in rotation:
                if tile not in table[edge]:
                    table[edge].append(tile)
    return table


def make_row_edge_table(rows: List[RotatedTile], side):
    table = defaultdict(list)
    for i, row in enumerate(rows):
        edge_val = row_edge(row, side)
        table[edge_val].append(i)
    return table


def row_edge(row, side):
    return tuple([rt.tile.edges[rt.rotation][side.value] for rt in row])


def solution1(tiles):
    edge_table = make_edge_table(tiles)
    singles = defaultdict(int)
    for edge, tile_list in edge_table.items():
        ids = [tile.id for tile in tile_list]
        if len(ids) == 1:
            singles[ids[0]] += 1

    corners = set()
    for s, count in singles.items():
        if count > 2:
            corners.add(s)

    print(corners)

    return reduce(lambda a, b: a * b, corners)


def debug(tile):
    print("DEBUG")
    print(f"{tile.id}: {tile.edges}")


def solution2(tiles):
    height = int(math.sqrt(len(tiles)))
    rows = make_rows(tiles, height)
    full = make_full(rows, height)
    grid = build_grid_from_rows(full)

    serpent = """
..................# 
#    ##    ##    ###
 #  #  #  #  #  #   """.strip()
    serpent_grid = grid_from_lines(serpent)
    shape_grids = [rotate_tile(serpent_grid.grid, n, width=serpent_grid.width, height=3) for n in range(8)]
    serpent_points = [points_from_grid(sg) for sg in shape_grids]

    count, points = count_overlapping_shapes(grid, serpent_points, width=12*8, height=12*8)

    print(f"found {count} serpents")
    return len(points)


def points_from_lines(lines, ch="#"):
    grid = grid_from_lines(lines)
    return points_from_grid(grid.grid)


def points_from_grid(grid, ch="#"):
    return set([p for p, v in grid.items() if v == ch])


def count_overlapping_shapes(grid, serpent_points_group, height, width):
    points = points_from_grid(grid)
    n = len(points)
    print(n)
    count = 0
    for serpent_points in serpent_points_group:
        for y in range(height):
            for x in range(width):
                serpent_p = set([(p[0] + x, p[1] + y) for p in serpent_points])
                intersect_count = len(serpent_p.intersection(points))
                if intersect_count == len(serpent_p):
                    count += 1
                    points.difference_update(serpent_p)
    return count, points


def rotate_tile(grid, rotation, width, height):
    # rotations:
    # 0 = None -> (x, y)
    # 1 = CW 90 -> (y, h-x)
    # 2 = CW 180
    # 3 = CW 270
    # 4 = None + flip
    # 5 = CW 90 + flip
    # 6 = CW 180 + flip
    # 7 = CW 270 + flip
    rows = grid_to_rows(grid, width, height)
    for _ in range(rotation % 4):
        # rotate 90 degrees CW
        rows = list(zip(*rows[::-1]))
    if rotation > 3:
        # flip
        rows = rows[::-1]
    return rows_to_grid(rows)


def grid_to_rows(grid, width=10, height=10):
    rows = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append(grid[(x, y)])
        rows.append(row)
    return rows


def rows_to_grid(rows):
    grid = dict()
    for y, row in enumerate(rows):
        for x, p in enumerate(row):
            grid[(x, y)] = p
    return grid


def build_grid_from_rows(rows):
    grid = dict()
    tile_size = 8
    border = 1
    width = height = border * 2 + tile_size
    for gy, row in enumerate(rows):
        for gx, rt in enumerate(row):
            tile_grid = rotate_tile(rt.tile.grid.grid, rt.rotation, width, height)
            place_tile_on_grid(gx * tile_size, gy * tile_size, border, tile_size, tile_grid, grid)

    return grid


def place_tile_on_grid(base_x, base_y, border, size, tile, grid):
    for x in range(border, border + size):
        for y in range(border, border + size):
            grid[(base_x + x - border, base_y + y - border)] = tile[(x, y)]


def render_full_ids(full):
    print("-" * 30)
    for row in full:
        row_ids = ["{}.{}".format(rt.tile.id, rt.rotation) for rt in row]
        print(" ".join(row_ids))
    print()
    print("-" * 30)


def extract_tile_ids(block, rows):
    tile_ids = set()
    for index in block:
        row = rows[index]
        for rt in row:
            tile_ids.add(rt.tile.id)
    return tile_ids


def make_full(rows, height):
    edge_table_tops = make_row_edge_table(rows, Side.TOP)

    blocks = defaultdict(list)
    blocks[1] = [[i] for i, row in enumerate(rows)]

    for size in range(2, height + 1):
        for b in blocks[size - 1]:
            contained_tiles = extract_tile_ids(b, rows)
            edge_to_match = row_edge(rows[b[-1]], Side.BOTTOM)
            matching_rows = edge_table_tops[edge_to_match]
            for row_index in matching_rows:
                if not contained_tiles.intersection(extract_tile_ids([row_index], rows)):
                    new_block = copy(b)
                    new_block.append(row_index)
                    blocks[size].append(new_block)
        print(f"Made {len(blocks[size])} blocks of size {size}")

    if not blocks[size]:
        raise RuntimeError(f"No solution found of size {size}")

    # for indices in blocks[size]:
    #     full = [rows[i] for i in indices]
    #     render_full_ids(full)

    ordered_rows = [rows[i] for i in blocks[size][0]]
    return ordered_rows


def make_rows(tiles, length):
    edge_table = make_edge_table(tiles)
    for edge, tile_list in edge_table.items():
        ids = [tile.id for tile in tile_list]
        # print(edge, ids)

    fragments = defaultdict(list)
    for tile in tiles:
        for rotation in range(8):
            fragments[1].append([RotatedTile(tile, rotation)])

    # print(len(fragments[1]))
    for size in range(2, length + 1):
        for f in fragments[size - 1]:
            tiles_in_f = [rt.tile for rt in f]
            end_tile = f[-1]
            # if end_tile.tile.id == 2311 or end_tile.tile.id == 3079:
            #     debug(end_tile.tile)
            edge_to_match = end_tile.tile.edges[end_tile.rotation][1]
            for matching_tile in edge_table[edge_to_match]:
                if matching_tile in tiles_in_f:
                    continue
                for rotation in range(8):
                    if matching_tile.edges[rotation][3] == edge_to_match:
                        new_fragment = copy(f)
                        new_fragment.append(RotatedTile(matching_tile, rotation))
                        fragments[size].append(new_fragment)
        print(f"Found {len(fragments[size])} fragments of size {size}")
        # for f in fragments[size]:
        #     parts = ["{}.{}".format(rt.tile.id, rt.rotation) for rt in f]
        #     print(" + ".join(parts))

    return fragments[length]


if __name__ == "__main__":
    run()

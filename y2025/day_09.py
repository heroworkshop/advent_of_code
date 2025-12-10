import itertools
import matplotlib.pyplot as plt

from y2025.day09_data import DATA

EXAMPLE = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
""".strip()

def parse(data):
    lines = [line.strip().split(",") for line in data.strip().split("\n")]
    return lines


def part1():
    rows = {tuple(map(int, x)) for x in parse(DATA)}

    for row in rows:
        print(row)

    pairs = itertools.combinations(rows, 2)
    # print(pairs)
    areas = [area(a, b) for a,b in pairs]
    # print(areas)

    return max(areas)


def area(a, b):
    return abs(a[0] - b[0] + 1) * abs(a[1] - b[1] + 1)

def part2():
    rows = [tuple(map(int, x)) for x in parse(EXAMPLE)]
    # nodes = set(rows)
    vertices = [(a, b) for a,b in zip(rows[:-1], rows[1:])]
    criticals = []
    for a, b in vertices:
        if abs(a[0] - b[0]) > 10000 or abs(a[1] - b[1]) > 10000:
            print(a, b)
            criticals.append((a, b))


    pairs = itertools.combinations(rows, 2)
    areas = {area(a, b): (a,b) for a,b in pairs if no_cross_vertices(a,b, vertices)}
    result = max(areas.keys())
    print(areas[result])
    visualize_polygon(rows, areas[result])
    assert result < 3071112100
    return result



Point = tuple[int, int]
Vertex = tuple[Point, Point]

def no_cross_vertices(a, b, polygon_vertices):
    ax, ay = a
    bx, by = b
    rect_vertices = [
        [(ax, ay), (bx, ay)],
        [(bx, ay), (bx, by)],
        [(bx, by), (ax, by)],
        [(ax, by), (ax, ay)],
    ]
    for (rx1, ry1), (rx2, ry2) in rect_vertices:
        for (px1, py1), (px2, py2) in polygon_vertices:
            px1, px2 = sorted([px1, px2])
            py1, py2 = sorted([py1, py2])
            if px1 < rx1 < px2 and py1 < ry1 < py2 < ry2 < py1 and px1 < rx2 < px2:
                return False
    return True

def pair_does_not_cross(a: Point, b: Point, criticals: list[Vertex]):
    for line in criticals:
        (x1, y1), (x2, y2) = line
        ax, ay = a
        bx, by =b
        if ay > y1 and by < y1:
            return False
    return True

def visualize_polygon(nodes, rect, title="Visualized Polygon"):
    """
    Visualizes a polygon given a list of integer coordinates.

    Args:
        nodes: A list of (x, y) tuples representing the ordered vertices
               of the polygon. Example: [(0, 0), (10, 0), (5, 5)]
        title: The title for the plot.
    """
    if not nodes:
        print("Error: The list of nodes is empty.")
        return

    # 1. Separate X and Y coordinates
    # Unzip the list of tuples into two lists: X and Y coordinates.
    x_coords = [node[0] for node in nodes]
    y_coords = [node[1] for node in nodes]

    # 2. Close the polygon
    # To close the shape, append the first coordinate to the end of the lists.
    # This draws the final edge from the last vertex back to the first.
    x_coords.append(x_coords[0])
    y_coords.append(y_coords[0])

    (rx1, ry1), (rx2, ry2) = rect
    rect_nodes = [(rx1, ry1), (rx2, ry1), (rx2, ry2), (rx1, ry2), (rx1, ry1)]
    rectx_coords = [node[0] for node in rect_nodes]
    recty_coords = [node[1] for node in rect_nodes]


    # 3. Create the plot
    plt.figure(figsize=(8, 6))

    # Plot the edges of the polygon
    plt.plot(x_coords, y_coords, marker='o', linestyle='-', color='blue', label='Polygon Edges')
    plt.plot(rectx_coords, recty_coords, marker='o', linestyle='-', color='green', label='Polygon Edges')

    # Plot the vertices as distinct points
    # (We use the original lists without the duplicated first point here)
    # plt.scatter(x_coords[:-1], y_coords[:-1], color='red', zorder=5, label='Vertices')

    # Add annotations for each vertex
    # for i, (x, y) in enumerate(nodes):
    #     plt.annotate(f'V{i + 1} ({x}, {y})', (x, y), textcoords="offset points",
    #                  xytext=(5, 5), ha='center', fontsize=9)

    # Set plot parameters
    plt.title(title)
    plt.xlabel("X-coordinate")
    plt.ylabel("Y-coordinate")
    plt.grid(True, linestyle='--')
    plt.axis('equal')  # Important: Ensures x and y axes have the same scale
    plt.legend()
    plt.show()

def max_inscribed_rectangle_rectilinear(nodes):
    """
    Calculates the largest area rectangle that can be inscribed within a
    rectilinear polygon defined by the given ordered list of nodes.

    The algorithm is O(n^2), where n is the number of vertices.

    Args:
        nodes: A list of (x, y) tuples representing the ordered vertices
               of the rectilinear polygon.

    Returns:
        A dictionary containing 'area', 'width', 'height', and 'bottom_left'
        of the largest rectangle found.
    """
    if len(nodes) < 4:
        return {"area": 0, "width": 0, "height": 0, "bottom_left": (0, 0)}

    # 1. Collect all unique x and y coordinates
    X = sorted(list(set(x for x, y in nodes)))
    Y = sorted(list(set(y for x, y in nodes)))

    # 2. Pre-process: Create a set of the polygon's vertices for quick lookup
    vertex_set = set(nodes)

    # Helper function to check if a point (x, y) is strictly inside the polygon
    # This uses the ray-casting algorithm (winding number check)
    def is_inside(px, py):
        # We only need to check if a point is strictly inside,
        # not on the boundary (as boundary checks are handled by coordinates).
        # Since this is a rectilinear polygon, we use a simpler containment check
        # based on segments, but for robustness, a full ray-casting is better.

        # NOTE: For complex polygons, this must be a full ray-casting.
        # For simple rectilinear polygons, we can often rely on a much simpler
        # check if we know the winding rule and the coordinate system.
        # However, for this problem, we rely on the grid points being checked
        # and the algorithm's constraints.

        # A simpler check for a rectangle's interior point (px, py)
        # We check if (px, py) is inside the bounding box of the polygon,
        # and then verify it doesn't cross any "inward-facing" edges.

        # For simplicity and given the rectilinear constraint, we assume that
        # if the coordinate lines (x=px, y=py) span across the polygon without
        # hitting an *interior* vertical or horizontal edge, the point is inside.

        # A quick-and-dirty method for rectilinear: check number of edge crossings
        # along a ray (e.g., ray to the right).
        crossings = 0
        for i in range(len(nodes)):
            x1, y1 = nodes[i]
            x2, y2 = nodes[(i + 1) % len(nodes)]

            if y1 == y2:  # Horizontal edge
                continue

            # Ensure y1 < y2 for upward ray check
            if y1 > y2:
                x1, y1, x2, y2 = x2, y2, x1, y1

            # Check if the horizontal ray from (px, py) crosses the segment (x1, y1) to (x2, y2)
            if y1 <= py < y2:
                # Calculate the x-coordinate of the intersection
                x_intersection = x1
                if px < x_intersection:
                    crossings += 1

        return crossings % 2 == 1

    max_area = 0
    best_rect = {"area": 0, "width": 0, "height": 0, "bottom_left": (0, 0)}

    # Iterate over all possible pairs of horizontal lines (y-coordinates)
    for i in range(len(Y)):
        y_bottom = Y[i]

        # For each y_bottom, consider all y_top lines above it
        for j in range(i + 1, len(Y)):
            y_top = Y[j]
            height = y_top - y_bottom

            # Use a technique similar to the Largest Rectangle in a Histogram
            # to find the widest span on the (y_bottom, y_top) strip.

            # The strip between y_bottom and y_top is broken by vertical edges
            # of the polygon that intersect this strip.

            # Collect all x-coordinates of vertical edges that span this height
            vertical_edge_x = []
            for k in range(len(nodes)):
                x1, y1 = nodes[k]
                x2, y2 = nodes[(k + 1) % len(nodes)]

                # Check for a vertical edge
                if x1 == x2:
                    # Check if the vertical edge spans or crosses the [y_bottom, y_top] interval
                    y_min = min(y1, y2)
                    y_max = max(y1, y2)

                    # If the edge is fully outside or just touches one endpoint, ignore it
                    if y_max > y_bottom and y_min < y_top:
                        vertical_edge_x.append(x1)

            # Add the overall min/max x-coordinates as boundaries
            x_min_poly = X[0]
            x_max_poly = X[-1]
            vertical_edge_x.extend([x_min_poly, x_max_poly])

            # Sort and deduplicate the vertical boundaries
            vertical_edge_x = sorted(list(set(vertical_edge_x)))

            # Check the midpoint of each resulting segment for containment
            # This is the "Largest Rectangle in a Histogram" part, where
            # the vertical boundaries define the "walls".

            for k in range(len(vertical_edge_x) - 1):
                x_left = vertical_edge_x[k]
                x_right = vertical_edge_x[k + 1]

                # Calculate the midpoint of the segment
                mid_x = (x_left + x_right) / 2.0
                mid_y = (y_bottom + y_top) / 2.0

                # If the midpoint is inside the polygon, the entire segment
                # between x_left and x_right is valid.
                if is_inside(mid_x, mid_y):
                    width = x_right - x_left
                    area = width * height

                    if area > max_area:
                        max_area = area
                        best_rect = {
                            "area": area,
                            "width": width,
                            "height": height,
                            "bottom_left": (x_left, y_bottom)
                        }

    return best_rect

if __name__ == "__main__":
    print("part1:", part1())
    print("part2:", part2())

from y2025.day_09 import node_is_inside_polygon

VERTICES = [((7, 1), (11, 1)),
            ((11, 1), (11, 7)),
            ((11, 7), (9, 7)),
            ((9, 7), (9, 5)),
            ((9, 5), (2, 5)),
            ((2, 5), (2, 3)),
            ((2, 3), (7, 3)),
            ((7, 3), (7, 1))]
MAXIMUMS = (20, 20)

def test_node_is_inside_polygon__for_node_outside_polygon__returns_false():
    result = node_is_inside_polygon((2, 11), VERTICES, *MAXIMUMS)
    assert result is False

def test_node_is_inside_polygon__for_node_inside_polygon__returns_false():
    result = node_is_inside_polygon((2, 3), VERTICES, *MAXIMUMS)
    assert result is True

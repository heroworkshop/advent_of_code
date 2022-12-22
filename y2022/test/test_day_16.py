import unittest

from assertpy import assert_that

from y2022.day_16 import make_nodes, solve_dual
from y2022.valve_solver import Node


class TestDualValveSolver(unittest.TestCase):
    def test_solver_split_path(self):
        nodes = make_nodes([
            Node(name='AA', rate=0, exits=['BB']),
            Node(name='BB', rate=0, exits=['DD', 'CC', 'AA']),
            Node(name='DD', rate=20, exits=['BB']),
            Node(name='CC', rate=10, exits=['BB']),
        ])
        solver = solve_dual(nodes, 13)
        for n in solver.best_path:
            print(n)
        path1 = [n.cur_node for n in solver.best_path]
        path2 = [n.ele_node for n in solver.best_path]
        assert_that(path1).is_equal_to(["BB", "CC", "CC"])
        assert_that(path2).is_equal_to(["BB", "DD", "DD"])
        assert_that(solver.best).is_equal_to(300)

    def test_solver_backtrack(self):
        nodes = make_nodes([
            Node(name='AA', rate=0, exits=['BB']),
            Node(name='BB', rate=1, exits=['DD', 'CC', 'AA']),
            Node(name='DD', rate=20, exits=['BB']),
            Node(name='CC', rate=10, exits=['BB']),
        ])
        solver = solve_dual(nodes, 13)
        for n in solver.best_path:
            print(n)
        assert_that(solver.best).is_equal_to(308)

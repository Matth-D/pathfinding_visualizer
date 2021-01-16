"""Dijkstra algorithm module."""
from . import algo_utils
from . import dijkstra  # pylint: disable=relative-beyond-top-level

algo_utils.append_libs()
import numpy as np


class Node:
    """Node class to populate algorithm grid."""

    def __init__(self, pos, g, h):
        self.pos = pos
        self.g_cost = g
        self.h_cost = h
        self.parent = None

    def __repr__(self):
        return "{}([{}, {}], {}, {}, {})".format(
            self.__class__.__name__, *self.pos, self.g_cost, self.h_cost, self.parent
        )


class BiDijkstra:
    """Class containing BiDijkstra Algorithm.

    Inputs:
        start_pos (tuple): Node start position.
        end_pos (tuple): Node end position.
        row_amount (integer): Number of rows in the grid.
        column_amount (integer): Number of columns in the grid.
        wall_pos (set, tuples): set position of obstacles
    """

    def __init__(self, start_pos, end_pos, row_amount, column_amount, wall_pos):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.row_amount = row_amount
        self.column_amount = column_amount
        self.wall_pos = wall_pos
        self.inf = float("inf")
        self.unvisited_pos = set()
        self.visited_pos = []
        self.path = []
        self.start_node = Node(start_pos, 0, self.inf)
        self.end_node = Node(end_pos, self.inf, self.inf)
        self.middle_node = None
        self.mix = {}

        # Init Grid
        self.grid = np.arange(row_amount * column_amount).reshape(
            row_amount, column_amount
        )
        self.grid = self.grid.astype("object")
        for i, x in enumerate(self.grid):
            for j, y in enumerate(x):
                self.grid[i, j] = Node((i, j), self.inf, self.inf)

        # Init nodes values
        for column in self.grid:
            for node in column:
                self.unvisited_pos.add(node.pos)
                if node.pos == self.start_pos:
                    self.start_node = node
                if node.pos == self.end_pos:
                    self.end_node = node
                node.g_cost = self.inf
                node.h_cost = self.inf
        self.start_node.g_cost = 0
        self.start_node.parent = "start"
        self.end_node.g_cost = 0
        self.end_node.parent = "end"

    def solve(self):
        """Perform Dijkstra algorithm given start node."""
        current_node = algo_utils.get_smallest_g_cost_unvisited_node(
            self.grid, self.unvisited_pos
        )
        if not current_node:
            return
        neighbours = algo_utils.get_neighbours(current_node, self.grid, self.wall_pos)
        if current_node.g_cost == self.inf:
            return

        for each in neighbours:
            if each.parent and each.parent != current_node.parent:
                self.middle_node = each
                self.visited_pos.append(each.pos)
                break

            current_dist = current_node.g_cost
            new_dist = current_dist + 1
            if each.g_cost < new_dist:
                continue
            each.g_cost = new_dist
            each.parent = current_node.parent
            mix_neigh = {each.pos: each.g_cost}
            self.mix.update(mix_neigh)
        mix_current = {current_node.pos: current_node.g_cost}
        self.mix.update(mix_current)

        if self.middle_node:
            self.visited_pos.append(current_node.pos)
            dijkstra_1 = dijkstra.Dijkstra(
                self.start_pos,
                self.middle_node.pos,
                self.row_amount,
                self.column_amount,
                self.wall_pos,
            )
            disjktra_2 = dijkstra.Dijkstra(
                self.middle_node.pos,
                self.end_pos,
                self.row_amount,
                self.column_amount,
                self.wall_pos,
            )
            dijkstra_1.solve()
            disjktra_2.solve()
            self.path = dijkstra_1.path + disjktra_2.path
            for key, value in self.mix.items():
                self.mix[key] = round((value * 1.0) / self.middle_node.g_cost, 3)
            return

        self.unvisited_pos.remove(current_node.pos)
        self.visited_pos.append(current_node.pos)
        if self.unvisited_pos:
            self.solve()


# start_pos = (0, 1)
# end_pos = (2, 3)
# wall_pos = [(0, 2), (1, 2)]
# row_amount = 3
# column_amount = 5
# ddij = BiDijkstra(start_pos, end_pos, row_amount, column_amount, wall_pos)
# ddij.solve()

# print(ddij.grid)
# ddij.solve()


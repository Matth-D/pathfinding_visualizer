"""Dijkstra algorithm module."""


from . import algo_utils


algo_utils.append_libs()

import numpy as np


class Node:
    """Node class to populate algorithm grid."""

    def __init__(self, pos, g):
        self.pos = pos
        self.g_cost = g

    def __repr__(self):
        return "{}([{},{}],{})".format(self.__class__.__name__, *self.pos, self.g_cost)


class Dijkstra:
    """Class containing Dijkstra Algorithm.

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
        self.start_node = Node(start_pos, 0)
        self.end_node = Node(end_pos, self.inf)
        self.mix = {}

        # Init Grid
        self.grid = np.arange(row_amount * column_amount).reshape(
            row_amount, column_amount
        )
        self.grid = self.grid.astype("object")
        for i, x in enumerate(self.grid):
            for j, y in enumerate(x):
                self.grid[i, j] = Node((i, j), self.inf)

        #     # Init nodes values
        for column in self.grid:
            for node in column:
                self.unvisited_pos.add(node.pos)
                if node.pos == self.start_pos:
                    self.start_node = node
                if node.pos == self.end_pos:
                    self.end_node = node
                node.g_cost = self.inf
        self.start_node.g_cost = 0

    def backtrack_path(self, current_node):
        """Return the shortest path by starting from end node."""
        self.path.insert(0, current_node.pos)
        neighbours = algo_utils.get_neighbours(current_node, self.grid, self.wall_pos)
        smallest_node = min(neighbours, key=lambda x: x.g_cost)
        if self.start_pos in self.path:
            return self.path
        else:
            current_node = smallest_node
            self.backtrack_path(current_node)

    def solve(self):
        """Perform Dijkstra algorithm given start node."""
        current_node = algo_utils.get_smallest_g_cost_unvisited_node(
            self.grid, self.unvisited_pos
        )
        if current_node.pos not in self.unvisited_pos:
            return
        if current_node.g_cost == self.inf:
            return
        neighbours = algo_utils.get_neighbours(current_node, self.grid, self.wall_pos)
        for neigh in neighbours:
            neighbour_dist = neigh.g_cost
            current_dist = current_node.g_cost
            new_dist = current_dist + 1
            if neighbour_dist < new_dist:
                continue
            neigh.g_cost = new_dist
            mix_neigh = {neigh.pos: neigh.g_cost}
            self.mix.update(mix_neigh)
        mix_current = {current_node.pos: current_node.g_cost}
        self.mix.update(mix_current)
        if (
            self.end_pos not in self.unvisited_pos
            or algo_utils.get_smallest_g_cost_unvisited_node(
                self.grid, self.unvisited_pos
            ).g_cost
            == self.inf
        ):
            for key, value in self.mix.items():
                self.mix[key] = round((value * 1.0) / self.end_node.g_cost, 3)
            self.backtrack_path(self.end_node)

        else:
            self.unvisited_pos.remove(current_node.pos)
            self.visited_pos.append(current_node.pos)
            current_node = algo_utils.get_smallest_g_cost_unvisited_node(
                self.grid, self.unvisited_pos
            )
            self.solve()


# start_pos = (0, 1)
# end_pos = (2, 3)
# wall_pos = [(0, 2), (1, 2)]
# row_amount = 3
# column_amount = 5
# dij = Dijkstra(start_pos, end_pos, row_amount, column_amount, wall_pos)

# dij.solve()


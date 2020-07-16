"""Dijkstra algorithm module."""
from . import dijkstra  # pylint: disable=relative-beyond-top-level


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
        self.grid = []
        for row in range(self.row_amount):
            self.grid.append([])
            for column in range(self.column_amount):
                node = Node((column, row), self.inf, self.inf)
                self.grid[row].append(node)

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

    def set_h_cost(self, node, goal_node):
        """Set heuristic cost for nodes to goal node."""
        if node.pos in self.wall_pos:
            node.h_cost = self.inf
            return
        node.h_cost = abs(node.pos[0] - goal_node.pos[0]) + abs(
            node.pos[1] - goal_node.pos[1]
        )

    def smallest_cost_node(self):
        """Return the smallest distance node in unvisited node set."""
        nodes = []
        for column in self.grid:
            for node in column:
                if node.pos in self.unvisited_pos:
                    nodes.append(node)
        return min(nodes, key=lambda x: x.g_cost)

    def get_neighbours(self, current_node):
        """Return neighbours from input node position based on grid size and wall_pos set."""
        neighbours_pos = set()
        for column, row in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            neighbor = (
                current_node.pos[0] + column,
                current_node.pos[1] + row,
            )
            if 0 <= neighbor[0] < self.column_amount:
                if 0 <= neighbor[1] < self.row_amount:
                    if neighbor not in self.wall_pos:
                        neighbours_pos.add(neighbor)
        neighbours = []
        for column in self.grid:
            for node in column:
                if node.pos in neighbours_pos:
                    neighbours.append(node)
        return neighbours

    def solve(self):
        """Perform Dijkstra algorithm given start node."""
        current_node = self.smallest_cost_node()
        if not current_node:
            return
        neighbours = self.get_neighbours(current_node)
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

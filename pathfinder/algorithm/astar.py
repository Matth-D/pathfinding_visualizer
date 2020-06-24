from PySide2 import QtWidgets, QtGui, QtCore


class Node:
    """Node Class containing attributes for pathfinding.

    Attributes:
        pos (tuple): Node position on the grid.
        g_cost (int) : Cost of travel from start node to current node.
        h_cost (int): Heuristic cost of travel from current node to end node.
        f_cost (int): Sum of g_cost and h_cost.
    """

    def __init__(self, pos, g, h):
        self.pos = pos
        self.g_cost = g
        self.h_cost = h

    @property
    def f_cost(self):
        return self.g_cost + self.h_cost

    def __repr__(self):
        return "{}([{},{}],{},{},{})".format(
            self.__class__.__name__, *self.pos, self.g_cost, self.h_cost, self.f_cost
        )


class Astar:
    """Class containing Astar Algorithm.

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
        self.start_node = Node(start_pos, 0, 0)
        self.end_node = Node(end_pos, self.inf, 0)

        # Init Grid
        self.grid = []
        for row in range(self.row_amount):
            self.grid.append([])
            for column in range(self.column_amount):
                node = Node((column, row), self.inf, 0)
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
        self.set_h_cost(self.start_node)

    def set_h_cost(self, node):
        """set heuristic cost for nodes to goal node"""

        node.h_cost = abs(node.pos[0] - self.end_node.pos[0]) + abs(
            node.pos[1] - self.end_node.pos[1]
        )

    def get_smallest_g_cost_unvisited_node(self):
        """Returns the smallest distance node in unvisited node set"""
        node_list = []
        for column in self.grid:
            for node in column:
                if node.pos in self.unvisited_pos:
                    node_list.append(node)
        return min(node_list, key=lambda x: x.g_cost)

    def get_smallest_h_cost_unvisited_node(self):
        """Returns the smallest h_cost node in unvisited node set"""
        node_list = []
        for column in self.grid:
            for node in column:
                if node.pos in self.unvisited_pos:
                    node_list.append(node)
        return min(node_list, key=lambda x: x.h_cost)

    def get_smallest_f_cost_unvisited_node(self):
        """Returns the smallest f_cost node in unvisited node set"""
        node_list = []
        for column in self.grid:
            for node in column:
                if node.pos in self.unvisited_pos:
                    node_list.append(node)
        min_f_cost_node = min(node_list, key=lambda x: x.g_cost)
        min_f_cost_list = []
        for column in self.grid:
            for node in column:
                if (
                    node.f_cost == min_f_cost_node.f_cost
                    and node.pos in self.unvisited_pos
                ):
                    min_f_cost_list.append(node)
        return min_f_cost_node, len(min_f_cost_list)

    def get_neighbours(self, current_node):
        """Returns neighbours from input node position based on grid size and wall_pos set"""
        neighbours_pos = set()
        for column, row in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            neighbor = (current_node.pos[0] + column, current_node.pos[1] + row)
            if 0 <= neighbor[0] < self.column_amount:
                if 0 <= neighbor[1] < self.row_amount:
                    if neighbor not in self.wall_pos:
                        neighbours_pos.add(neighbor)
        neighbours = set()
        for column in self.grid:
            for node in column:
                if node.pos in neighbours_pos:
                    neighbours.add(node)
        return neighbours

    def backtrack_path(self, current_node):
        """Return the shortest path by starting from end node"""
        self.path.insert(0, current_node.pos)
        neighbours = self.get_neighbours(current_node)
        n_copy = list(neighbours)
        for n in n_copy:
            if n.pos not in self.visited_pos:
                n_copy.remove(n)
        neighbours = n_copy.copy()
        smallest_node = min(neighbours, key=lambda x: x.g_cost)
        if self.start_pos in self.path:
            return self.path
        else:
            current_node = smallest_node
            self.backtrack_path(current_node)

    def solve(self):
        """Permforms Astar algorithm at a given start node"""
        smallest_f = self.get_smallest_f_cost_unvisited_node()
        smallest_f_node = smallest_f[0]

        if smallest_f[1] > 1:
            current_node = self.get_smallest_h_cost_unvisited_node()
        else:
            current_node = smallest_f_node
        if current_node.f_cost == self.inf:
            return

        self.set_h_cost(current_node)
        self.unvisited_pos.remove(current_node.pos)
        self.visited_pos.append(current_node.pos)
        neighbours = self.get_neighbours(current_node)

        for neigh in neighbours:
            neighbour_dist = neigh.g_cost
            current_dist = current_node.g_cost
            new_dist = current_dist + 1
            if neighbour_dist < new_dist:
                continue
            neigh.g_cost = new_dist
            self.set_h_cost(neigh)

        smallest_f = self.get_smallest_f_cost_unvisited_node()
        smallest_f_node = smallest_f[0]
        smallest_h_node = self.get_smallest_h_cost_unvisited_node()

        if (
            self.end_pos not in self.unvisited_pos
            or self.get_smallest_g_cost_unvisited_node() == self.inf
        ):
            self.backtrack_path(self.end_node)
        else:
            if smallest_f[1] > 1:
                current_node = smallest_h_node
            else:
                current_node = smallest_f_node
            self.solve()

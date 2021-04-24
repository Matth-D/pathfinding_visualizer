import os
import sys

"""Module containing methods common to three algorithms"""


def append_libs():
    """Append user libs to sys.path."""
    libs_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "libs")
    libs_path = os.path.abspath(libs_path)

    if libs_path not in sys.path:
        sys.path.append(libs_path)


def get_smallest_g_cost_unvisited_node(grid, unvisited_pos):
    """Get the smallest unvisited node by g_cost.

    Args:
        grid (array): 2d array representing grid.
        unvisited_pos (list): List of unvisited position in the graph.

    Returns:
        obj: Smallest unvisited node object.
    """
    node_list = []
    for column in grid:
        for node in column:
            if node.pos in unvisited_pos:
                node_list.append(node)
    return min(node_list, key=lambda x: x.g_cost)


def get_neighbours(current_node, grid, wall_pos):
    """Get current_node neighbours in a 2d array.

    Args:
        current_node (object): Current Node in the solve step.
        grid (list): 2d array of all nodes.
        wall_pos (list): List of tuples of walls in the graph.

    Returns:
        list: List of current node neighbours.
    """
    row_amount = grid.shape[0]
    column_amount = grid.shape[1]
    neighbours_pos = set()
    for column, row in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        neighbor = (current_node.pos[0] + column, current_node.pos[1] + row)
        if 0 <= neighbor[0] < row_amount:
            if 0 <= neighbor[1] < column_amount:
                if neighbor not in wall_pos:
                    neighbours_pos.add(neighbor)
    neighbours = set()
    for column in grid:
        for node in column:
            if node.pos in neighbours_pos:
                neighbours.add(node)
    return neighbours

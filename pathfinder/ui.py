"""Shortest Path Visualizer."""
# -*- coding: utf-8 -*-
import time
import sys
import math
from PySide2 import QtWidgets, QtGui, QtCore
from .algorithm import astar, dijkstra, bidijkstra

sys.setrecursionlimit(2000)


class DrawGrid(QtWidgets.QWidget):
    """Create custom widget to draw grid based on grid_widget dimensions."""

    def __init__(self, *args, **kwargs):
        self.cell_size = kwargs.pop("cell_size", 20)
        self.algorithm_value = kwargs.pop("algorithm", "DIJKSTRA")
        super().__init__(*args, **kwargs)
        self.threadpool = QtCore.QThreadPool()
        self.start_pos = (-1, -1)
        self.wall_pos = set()
        self.end_pos = (-1, -1)
        self.current = None
        self.visited_pos = []
        self.shortest_path = []
        self.algorithm = None
        self.click = None
        self.grid_width = None
        self.grid_height = None
        self.row_amount = None
        self.column_amount = None

    def paintEvent(self, event):  # pylint: disable=invalid-name, unused-argument
        """Paint grid event."""
        painter = QtGui.QPainter()
        painter.begin(self)
        self.draw_rectangles(painter)
        painter.end()

    def mouseMoveEvent(self, event):  # pylint: disable=invalid-name, unused-argument
        """Handle mouse move event."""
        mouse_coordinates = (event.x(), event.y())
        clicked_cell = self.get_clicked_cell(mouse_coordinates)
        self.set_current_coordinates(clicked_cell)
        if event.button() == QtCore.Qt.RightButton:
            self.click = "right"
        if event.button() == QtCore.Qt.LeftButton:
            self.click = "left"

        self.update()

    def mousePressEvent(self, event):  # pylint: disable=invalid-name
        """Handle mouse press event."""
        mouse_coordinates = (event.x(), event.y())
        clicked_cell = self.get_clicked_cell(mouse_coordinates)
        self.set_current_coordinates(clicked_cell)
        if event.button() == QtCore.Qt.RightButton:
            self.click = "right"
        if event.button() == QtCore.Qt.LeftButton:
            self.click = "left"
        self.update()

    def set_current_coordinates(self, coordinates):
        """Set which cell to draw."""
        if self.current == "start":
            self.start_pos = coordinates
        elif self.current == "end":
            self.end_pos = coordinates
        elif self.current == "wall":
            self.wall_pos.add(coordinates)
            if self.click == "right" and coordinates in self.wall_pos:
                self.wall_pos.remove(coordinates)

    def set_start(self):
        """Set current to start."""
        self.current = "start"

    def set_end(self):
        """Set current to end."""
        self.current = "end"

    def set_walls(self):
        """Set current to walls."""
        self.current = "wall"

    def get_clicked_cell(self, coordinates):
        """Return cell coordinates from click coordinates."""
        max_x = self.cell_size * self.column_amount
        max_y = self.cell_size * self.row_amount
        if coordinates[0] > max_x or coordinates[1] > max_y:
            return (-1, -1)
        clicked_column = math.floor((coordinates[0] / max_x) * self.column_amount)
        clicked_row = math.floor((coordinates[1] / max_y) * self.row_amount)
        return (clicked_column, clicked_row)

    def set_cell_size(self, value):
        """Set cell size."""
        self.cell_size = value
        self.update()

    def set_algorithm(self, value):
        """Set algorithm to solve."""
        self.algorithm_value = value
        args = [
            self.start_pos,
            self.end_pos,
            self.row_amount,
            self.column_amount,
            self.wall_pos,
        ]
        if self.algorithm_value == "DIJKSTRA":
            self.algorithm = dijkstra.Dijkstra(*args)
        if self.algorithm_value == "A*":
            self.algorithm = astar.Astar(*args)
        if self.algorithm_value == "BIDIRECTIONAL DIJKSTRA":
            self.algorithm = bidijkstra.BiDijkstra(*args)

    def solve_algorithm(self):
        """Solve selected algorithm."""
        if self.visited_pos:
            return
        self.set_algorithm(self.algorithm_value)
        self.algorithm.solve()

        for each in self.algorithm.visited_pos:
            self.visited_pos.append(each)
            self.update_draw()

        for each in self.algorithm.path:
            self.shortest_path.append(each)
            self.update_draw()

    def update_draw(self):
        """Process event when item added to visited pos/shortest path list."""
        QtWidgets.QApplication.processEvents()
        self.update()
        time.sleep(0.003)

    def reset_grid(self):
        """Reset algo values."""
        self.wall_pos = set()
        self.visited_pos = []
        self.shortest_path = []
        self.update()

    def draw_rectangles(self, painter):
        """Draw the grid based on algo data."""
        self.grid_width = self.width()
        self.grid_height = self.height()
        self.row_amount = math.floor(self.grid_height / self.cell_size)
        self.column_amount = math.floor(self.grid_width / self.cell_size)
        painter.setPen(QtGui.QColor(44, 62, 80))
        for column in range(self.column_amount):
            for row in range(self.row_amount):
                color = QtGui.QColor(247, 242, 235)
                if (column, row) in self.wall_pos:
                    color = QtGui.QColor(26, 37, 48)
                if (column, row) in self.visited_pos:
                    color = QtGui.QColor(231, 76, 60)
                if (column, row) in self.shortest_path:
                    color = QtGui.QColor(106, 235, 159)
                if (column, row) == self.start_pos:
                    color = QtGui.QColor(131, 193, 243)
                if (column, row) == self.end_pos:
                    color = QtGui.QColor(36, 103, 178)
                painter.setBrush(color)
                painter.drawRect(
                    self.cell_size * column,
                    self.cell_size * row,
                    self.cell_size,
                    self.cell_size,
                )


class ShortestPathVisualizer(QtWidgets.QDialog):
    """Create UI for shortest path visualizer."""

    def __init__(self):
        super(ShortestPathVisualizer, self).__init__()
        self.algorithm_type = ["A*", "DIJKSTRA", "BIDIRECTIONAL DIJKSTRA"]
        self.selected_algorithm = self.algorithm_type[0]
        self.init_ui()
        self.setGeometry(300, 300, self.app_size[0], self.app_size[1])
        self.setWindowTitle("Shortest Path Visualizer")
        self.center_window()

    def init_ui(self):
        """Init UI layout."""
        desktop = QtWidgets.QDesktopWidget()
        self.screen_size = desktop.availableGeometry(desktop.primaryScreen())
        self.app_size = (
            round(self.screen_size.width() * 0.9),
            round(self.screen_size.height() * 0.8),
        )
        # --------------------------- Create layout here
        self.setStyleSheet("background-color:rgb(44, 62, 80)")
        self.main_layout = QtWidgets.QVBoxLayout(self)

        self.density_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.density_slider.setMinimum(22)
        default_cell_size = 50
        self.density_slider.setValue(default_cell_size)
        self.grid_widget = DrawGrid(
            self, cell_size=default_cell_size, algorithm=self.selected_algorithm
        )
        self.density_slider.valueChanged.connect(self.grid_widget.set_cell_size)
        self.layout_h1 = QtWidgets.QHBoxLayout()

        self.main_layout.addWidget(self.density_slider)
        self.main_layout.addWidget(self.grid_widget)
        self.main_layout.addLayout(self.layout_h1)

        self.pick_start_button = QtWidgets.QPushButton("PICK START", self)
        self.pick_start_button.setStyleSheet(
            "font:Fira Code;font-size:15px;background-color:rgb(231, 76, 60);color:white"
        )

        self.draw_walls_button = QtWidgets.QPushButton("DRAW WALLS", self)
        self.draw_walls_button.setStyleSheet(
            "font-size:15px;background-color:rgb(231, 76, 60);color:white"
        )
        self.algorithm_list = QtWidgets.QComboBox()
        self.algorithm_list.addItems(self.algorithm_type)
        css = """
            font-size:15px;
            background-color:rgb(231, 76, 60);
            color:white;
            selection-background-color:rgb(255, 126, 110)
        """
        self.algorithm_list.setStyleSheet(css)
        self.algorithm_list.currentTextChanged.connect(self.grid_widget.set_algorithm)

        self.horizontal_spacer_1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.pick_end_button = QtWidgets.QPushButton("PICK END", self)
        self.pick_end_button.setStyleSheet(
            "font-size:15px;background-color:rgb(231, 76, 60);color:white"
        )

        self.run_button = QtWidgets.QPushButton("RUN", self)
        self.run_button.setStyleSheet(
            "font-size:15px;background-color:rgb(231, 76, 60);color:white"
        )
        self.reset_button = QtWidgets.QPushButton("RESET", self)
        self.reset_button.setStyleSheet(
            "font-size:15px;background-color:rgb(231, 76, 60);color:white"
        )
        self.layout_h1.addWidget(self.pick_start_button)
        self.layout_h1.addWidget(self.pick_end_button)
        self.layout_h1.addWidget(self.draw_walls_button)
        self.layout_h1.addWidget(self.algorithm_list)
        self.layout_h1.addItem(self.horizontal_spacer_1)
        self.layout_h1.addWidget(self.run_button)
        self.layout_h1.addWidget(self.reset_button)
        self.layout_h1.setSpacing(10)
        self.layout_h1.setContentsMargins(0, 0, 10, 0)

        self.pick_start_button.clicked.connect(self.grid_widget.set_start)
        self.pick_end_button.clicked.connect(self.grid_widget.set_end)
        self.draw_walls_button.clicked.connect(self.grid_widget.set_walls)
        self.run_button.clicked.connect(self.grid_widget.solve_algorithm)
        self.reset_button.clicked.connect(self.grid_widget.reset_grid)

        # Closes app with Ctrl+Q shortcut
        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+Q"), self)
        shortcut.activated.connect(self.close)

    def center_window(self):
        """Centers window on screen."""
        app_geo = self.frameGeometry()
        center_point = QtWidgets.QDesktopWidget().availableGeometry().center()
        app_geo.moveCenter(center_point)
        self.move(app_geo.topLeft())


def main():
    """Set main program function."""
    app = QtWidgets.QApplication(sys.argv)
    shortest_path_visualizer = ShortestPathVisualizer()
    shortest_path_visualizer.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

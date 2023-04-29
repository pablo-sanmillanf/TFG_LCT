from typing import List, Any

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib import ticker
from scipy.interpolate import interp1d
import numpy as np
from matplotlib.backend_bases import MouseButton, MouseEvent
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar
)
from matplotlib.figure import Figure
import matplotlib

matplotlib.use('Qt5Agg')


class MplLine:
    """
    This class is used to plot a number of points and a smooth line to join them with the same color as the points.
    """
    def __init__(self, axis: matplotlib.axes.Axes, x: np.ndarray, y: np.ndarray) -> None:
        """
        Creates MplLine object. Is composed of a number of points passed in the x and y variables and a smooth line
        that join them.
        :param axis: The axis were the object will be plotted. Can't be None.
        :param x: A numpy array with the x-values.
        :param y: A numpy array with the y-values.
        """
        self.axis = axis

        # plot the x and y using scatter function
        self.data = self.axis.scatter(x, y, marker="o", picker=10)

        self.color = self.data.get_facecolors()[0].tolist()

        if len(x) > 1:
            # Create smooth union points line
            if len(x) > 2:
                interpolation_model = interp1d(x, y, kind="quadratic")
            else:
                interpolation_model = interp1d(x, y, kind="linear")
            smooth_x = np.linspace(np.amin(x), np.amax(x), len(x)*50)
            smooth_y = interpolation_model(smooth_x)
            self.smooth_line = self.axis.plot(smooth_x, smooth_y, color=self.color)[0]

    def set_visible(self, state: bool) -> None:
        """
        Set the smooth line and the points visible or invisible depending on the state.
        :param state: If True, elements visible. If False, elements invisible.
        """
        self.data.set_visible(state)
        self.smooth_line.set_visible(state)

    def get_data(self) -> matplotlib.collections.PathCollection:
        """
        Returns the points-data.
        :return: An object with the data of the points.
        """
        return self.data

    def get_smooth_line(self) -> matplotlib.lines.Line2D:
        """
        Returns a Line2D that represents the smooth line that joins the points.
        :return: The smooth line object.
        """
        return self.smooth_line

    def get_color(self) -> list[int]:
        return self.color

    def __del__(self):
        self.data.remove()
        self.smooth_line.remove()


class MplCanvas(FigureCanvas):
    """
    This class represents the Matplotlib canvas in which all the graphs will be plotted. This canvas is Qt compatible.
    """
    axes: matplotlib.axes.Axes

    def __init__(self, graph_visible_points: int, init_x: int = 0, parent: QWidget = None,
                 width: int = 8, height: int = 5, dpi: int = 100) -> None:
        """
        Creates MplCanvas object. It will be the canvas where the graphs will be plotted.
        :param graph_visible_points: The number of visible points in the x-axis in the figure.
        :param init_x: The start x point.
        :param parent: The QWidget that contains this object.
        :param width: The object width in inches.
        :param height: The object height in inches.
        :param dpi: The number of dots per inch. Represents the quality of the graph.
        """
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.axes = self.figure.add_subplot(111)

        self.figure.subplots_adjust(right=0.975)

        self.graph_visible_points = graph_visible_points

        self.axes.grid()

        # Set Y step
        self.axes.xaxis.set_major_locator(ticker.MultipleLocator(1))

        # Set Y values
        self.axes.set_yticks(np.arange(1, 5))
        self.axes.set_ylim(bottom=0.25, top=4.75)

        self.axes.set_xlim(left=init_x, right=init_x + graph_visible_points)

    def set_visible_points(self, visible_points: int) -> None:
        self.graph_visible_points = visible_points
        self.axes.set_xlim(left=0, right=visible_points)
        self.draw()


class MplWidget(QWidget):
    """
    This class is used to create an embedded matplotlib graph in a Qt environment.
    """
    lines: list[MplLine]

    pos_changed = pyqtSignal(int)
    point_clicked = pyqtSignal(int)

    def __init__(self, parent, graph_visible_points: int = 10) -> None:
        """
        Creates a MplWidget object.
        :param graph_visible_points: The number of visible points in the x-axis in the graph.
        """
        super().__init__(parent)

        self.canvas = MplCanvas(graph_visible_points, parent=self)
        self.toolbar = NavigationToolbar(self.canvas, None)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.canvas)
        self.lines = []

        self.secondary_axes = []

        self.tolerance = 0.2

        self.canvas.mpl_connect("button_press_event", self.on_press)
        self.canvas.mpl_connect("button_release_event", self.on_release)
        self.canvas.mpl_connect("motion_notify_event", self.on_move)

        self.max_len = 0

        self.clicked = False
        self.movement_clicked = False
        self.start_panning_point = 0
        self.left_x_lim = 0
        self.right_x_lim = 0
        self.panning_multiplier = 0

    def set_visible_points(self, visible_points: int) -> None:
        self.canvas.set_visible_points(int(visible_points))

    def set_graph_visible(self, graph_index: int, visible: bool):
        if graph_index < len(self.lines):
            self.lines[graph_index].set_visible(visible)
            self.canvas.draw()

    def add_graph(self, x: np.ndarray, y: np.ndarray, labels: list[str] | np.ndarray) -> None:
        """
        Add a graph to the canvas. The  points of the graph will be joined with a smooth line of the same color.
        :param x: The x values to plot.
        :param y: The y values to plot.
        :param labels: The labels to set in the y-axis. Must be of length 4.
        """
        if len(labels) != 4:
            raise Exception("Length labels must be 4")

        self.lines.append(MplLine(self.canvas.axes, x, y))

        line_color = self.lines[-1].get_color()

        # Resize slider movement to adjust to graph length
        if len(x) > self.max_len:
            self.max_len = len(x)

        if len(self.lines) == 1:

            # Add custom Y-labels
            self.canvas.axes.set_yticklabels(labels)

            # Setting up Y-axis tick color
            self.canvas.axes.spines['left'].set_color(line_color)

            # Setting up X-axis tick color
            self.canvas.axes.tick_params(axis='y', colors=line_color)
        else:

            self.secondary_axes.append(self.canvas.axes.secondary_yaxis(
                - (len(self.lines) - 1) * 0.1,
                functions=(lambda x_sec: x_sec, lambda x_sec: x_sec)
            ))

            # Set Y values
            self.secondary_axes[-1].set_yticks(np.arange(1, 5))

            # Add custom Y-labels
            self.secondary_axes[-1].set_yticklabels(labels)

            # Setting up Y-axis tick color
            self.secondary_axes[-1].spines['left'].set_color(line_color)

            # Setting up X-axis tick color
            self.secondary_axes[-1].tick_params(axis='y', colors=line_color)

            self.canvas.figure.subplots_adjust(left=0.15 + (len(self.lines) - 2) * 0.065)
        self.canvas.draw()

    def remove_graphs(self) -> None:
        """
        Add a graph to the canvas. The  points of the graph will be joined with a smooth line of the same color.
        """
        self.lines.clear()
        for sec_axis in self.secondary_axes:
            sec_axis.remove()
        self.secondary_axes.clear()
        self.canvas.draw()

        # Reset color cycle
        self.canvas.axes.set_prop_cycle(None)

    def save_figure(self, s: bool):
        self.toolbar.save_figure(s)

    def on_press(self, event: MouseEvent) -> None:
        """
        This function will control when the mouse Left button is pressed and will enable the panning function.
        :param event: The MouseEvent
        """
        if event.button is MouseButton.LEFT:
            self.clicked = True
            self.start_panning_point = event.x
            self.left_x_lim,  self.right_x_lim = self.canvas.axes.get_xlim()

            # The 1.3 factor is a correction factor based on trial and error to adjust movement speed.
            self.panning_multiplier = 1.3 * (self.right_x_lim - self.left_x_lim) / self.width()

    def on_release(self, event: MouseEvent) -> None:
        """
        This function will control when the mouse Left button is released and will disable the panning function.
        :param event: The MouseEvent
        """
        if event.button is MouseButton.LEFT:
            self.clicked = False
            if self.movement_clicked:
                self.movement_clicked = False
            else:
                canvas_width, canvas_height = self.canvas.get_width_height()
                axis_x0, axis_y0, axis_width, axis_height = self.canvas.axes.get_position().bounds

                x_pos = event.x / canvas_width
                y_pos = event.y / canvas_height
                if (axis_x0 <= x_pos <= axis_x0 + axis_width) and (axis_y0 <= y_pos <= axis_y0 + axis_height):
                    x_lims = self.canvas.axes.get_xlim()
                    x_pos = (x_pos - axis_x0) / axis_width * (x_lims[1] - x_lims[0]) + x_lims[0]

                    if abs(x_pos - np.around(x_pos)) <= self.tolerance:
                        self.point_clicked.emit(int(np.around(x_pos)))

    def on_move(self, event: MouseEvent) -> None:
        """
        This function will control the movement of the cursor when the mouse Left button is pressed and will pan the
        matplotlib canvas accordingly.
        :param event: The MouseEvent
        """
        if self.clicked:
            self.movement_clicked = True
            gap_moved = (event.x - self.start_panning_point) * self.panning_multiplier
            self.canvas.axes.set_xlim(left=self.left_x_lim - gap_moved, right=self.right_x_lim - gap_moved)
            self.canvas.draw()

            # Change slider position according to the panning position
            slider_val = int((self.left_x_lim - gap_moved) * 99 / (self.max_len - self.canvas.graph_visible_points))
            if slider_val < 0:
                slider_val = 0
            elif slider_val > 99:
                slider_val = 99
            self.pos_changed.emit(slider_val)

    def position_changed_slot(self, value: int) -> None:
        """
        This slot is used to change graph x-position based on a slider position.
        :param value: The slider position between 0 and 99
        """
        adjusted_val = value * (self.max_len - self.canvas.graph_visible_points) / 99
        self.canvas.axes.set_xlim(left=adjusted_val, right=adjusted_val + self.canvas.graph_visible_points)
        self.canvas.draw()


"""
zoomact = QAction(QIcon("zoom.png"), "save", self)
zoomact.setShortcut("Ctrl+s")
zoomact.triggered.connect(self.mpl_toolbar.save_figure)

self.toolbar = self.addToolBar("save")
self.toolbar.addAction(zoomact)
"""
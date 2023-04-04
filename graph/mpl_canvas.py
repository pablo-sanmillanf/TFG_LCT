from PyQt5.QtWidgets import QWidget, QVBoxLayout
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
    def __init__(self, axis, x, y):
        self.axis = axis

        # plot the x and y using scatter function
        self.data = self.axis.scatter(x, y, marker="o", picker=10)

        self.color = self.data.get_facecolors()[0].tolist()

        # Create smooth union points line
        interpolation_model = interp1d(x, y, kind="quadratic")
        smooth_x = np.linspace(x.min(), x.max(), len(x)*50)
        smooth_y = interpolation_model(smooth_x)
        self.smooth_line = self.axis.plot(smooth_x, smooth_y, color=self.color)[0]

    def set_visible(self, state):
        self.data.set_visible(state)
        self.smooth_line.set_visible(state)

    def get_data(self):
        return self.data

    def get_smooth_line(self):
        return self.smooth_line

    def get_color(self):
        return self.color


class MplCanvas(FigureCanvas):
    axes: matplotlib.axes.Axes

    def __init__(self, graph_visible_points, init_x=0, parent=None, width=8, height=5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.axes = self.figure.add_subplot(111)

        self.figure.subplots_adjust(right=0.975)

        self.axes.grid()

        # Set Y values
        self.axes.set_yticks(np.arange(1, 5))
        self.axes.set_ylim(bottom=0.25, top=4.75)

        self.axes.set_xlim(left=init_x, right=init_x + graph_visible_points)


class MplWidget(QWidget):
    def __init__(self, graph_visible_points=10):
        super().__init__()

        self.canvas = MplCanvas(graph_visible_points, parent=self)
        self.toolbar = NavigationToolbar(self.canvas, None)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.canvas)
        self.lines = []

        self.canvas.mpl_connect("button_press_event", self.on_press)
        self.canvas.mpl_connect("button_release_event", self.on_release)
        self.canvas.mpl_connect("motion_notify_event", self.on_move)

        self.clicked = False
        self.start_panning_point = 0
        self.left_x_lim = 0
        self.right_x_lim = 0
        self.panning_multiplier = 0

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

        if len(self.lines) == 1:

            # Add custom Y-labels
            self.canvas.axes.set_yticklabels(labels)

            # Setting up Y-axis tick color
            self.canvas.axes.spines['left'].set_color(line_color)

            # Setting up X-axis tick color
            self.canvas.axes.tick_params(axis='y', colors=line_color)
        else:

            sec_axis = self.canvas.axes.secondary_yaxis(
                - (len(self.lines) - 1) * 0.1,
                functions=(lambda x_sec: x_sec, lambda x_sec: x_sec)
            )

            # Set Y values
            sec_axis.set_yticks(np.arange(1, 5))

            # Add custom Y-labels
            sec_axis.set_yticklabels(labels)

            # Setting up Y-axis tick color
            sec_axis.spines['left'].set_color(line_color)

            # Setting up X-axis tick color
            sec_axis.tick_params(axis='y', colors=line_color)

            self.canvas.figure.subplots_adjust(left=0.15 + (len(self.lines) - 2) * 0.065)

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

    def on_move(self, event: MouseEvent) -> None:
        """
        This function will control the movement of the cursor when the mouse Left button is pressed and will pan the
        matplotlib canvas accordingly.
        :param event: The MouseEvent
        """
        if self.clicked:
            gap_moved = (event.x - self.start_panning_point) * self.panning_multiplier
            self.canvas.axes.set_xlim(left=self.left_x_lim - gap_moved, right=self.right_x_lim - gap_moved)
            self.canvas.draw()




"""
zoomact = QAction(QIcon("zoom.png"), "save", self)
zoomact.setShortcut("Ctrl+s")
zoomact.triggered.connect(self.mpl_toolbar.save_figure)

self.toolbar = self.addToolBar("save")
self.toolbar.addAction(zoomact)
"""
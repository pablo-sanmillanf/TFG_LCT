# Import libraries using import keyword
import numpy as np
from scipy.interpolate import interp1d
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from matplotlib.widgets import Slider
from matplotlib.backend_tools import ToolBase


def on_hover(event, axis, highlight_line):
    if event.inaxes is not None:
        if event.inaxes == axis:
            x = event.xdata
            y = event.ydata
            tolerance = 0.1
            if abs(x - np.around(x)) <= tolerance:
                for line in event.inaxes.get_lines():
                    if line == highlight_line:
                        line.set_xdata(np.full(len(line.get_xdata()), np.around(x)))
                        line.set_visible(True)
                        event.canvas.draw()


def on_click(event, axis):
    if event.inaxes is not None:
        if event.inaxes == axis and event.button == matplotlib.backend_bases.MouseButton.RIGHT:
            x = event.xdata
            y = event.ydata
            tolerance = 0.1
            if abs(x - np.around(x)) <= tolerance:
                print(f"Open the menu\tCoords: X: {x}, Y: {y}")


# Custom Axis to don't allow Y movement

class My_Axes(matplotlib.axes.Axes):
    name = "My_Axes"

    def drag_pan(self, button, key, x, y):
        matplotlib.axes.Axes.drag_pan(self, button, 'x', x, y)  # pretend key=='x'


matplotlib.projections.register_projection(My_Axes)

matplotlib.rcParams['toolbar'] = 'toolmanager'


class ShowHideTool(ToolBase):
    """
    Show and hide all the graphs sequentially in this order and 
    in a cyclical manner (with n, the number of existing graphs):
        -Show all.
        -Show graph 1.
        -Show graph 2.
        ...
        -Show graph n.
    """
    default_keymap = 'v'  # keyboard shortcut
    description = 'Change graphs showed'

    def __init__(self, *args, axis, graphs, **kwargs):
        self.axis = axis
        self.graphs = graphs
        self.show_all = False
        self.index = 0
        super().__init__(*args, **kwargs)

    def trigger(self, *args, **kwargs):
        if self.show_all and self.index == 0:
            self.show_all = False
            for graph in self.graphs:
                graph.set_visible(True)
        else:
            # Set all non-visible excepts one
            for i in range(len(self.graphs)):
                if i == self.index:
                    self.graphs[i].set_visible(True)
                else:
                    self.graphs[i].set_visible(False)

            if self.index == 0:
                self.show_all = True

            self.index = (self.index + 1) % len(self.graphs)

        # Update visible graphs
        self.figure.canvas.draw()


class Graph:
    def __init__(self, axis, x, y):
        self.axis = axis

        # plot the x and y using scatter function
        self.data = self.axis.scatter(x, y, marker="o", picker=10)

        self.color = self.data.get_facecolors()[0].tolist()

        # Create smooth union points line
        cubic_interpolation_model = interp1d(x, y, kind="cubic")
        X_ = np.linspace(x.min(), x.max(), len(x)*10)
        Y_ = cubic_interpolation_model(X_)
        self.smooth_line = self.axis.plot(X_, Y_, color=self.color)[0]

    def set_visible(self, state):
        self.data.set_visible(state)
        self.smooth_line.set_visible(state)

    def get_data(self):
        return self.data

    def get_smooth_line(self):
        return self.smooth_line

    def get_color(self):
        return self.color


class GraphPlotter:
    def __init__(self, allow_float=False, graph_visible_points=10, number_of_graphs = 2):
        self.allow_float = allow_float
        self.graph_visible_points = graph_visible_points
        self.graphs = np.empty(number_of_graphs, dtype=type(Graph))
        self.graphs_added = 0

        # Max default graph length to adjust the slider movement to the function 
        self.max_graph_len = 100

        # Setting Fig and Axis variables as subplots()
        # function returns tuple(fig, ax)
        self.fig, self.axis = plt.subplots(subplot_kw={"projection": "My_Axes"}, figsize=(9, 6))

        self.highlight_line = self.axis.axvline(0, linestyle='-', color='red')
        self.highlight_line.set_visible(False)

        # Set mouse  action 
        self.fig.canvas.mpl_connect('motion_notify_event', lambda event: on_hover(event, self.axis, self.highlight_line))
        self.fig.canvas.mpl_connect('button_press_event', lambda event: on_click(event, self.axis))

        # Remove the useless buttons from toolbar
        self.fig.canvas.manager.toolmanager.remove_tool('home')
        self.fig.canvas.manager.toolmanager.remove_tool('back')
        self.fig.canvas.manager.toolmanager.remove_tool('forward')
        self.fig.canvas.manager.toolmanager.remove_tool('zoom')
        self.fig.canvas.manager.toolmanager.remove_tool('subplots')
        self.fig.canvas.manager.toolmanager.remove_tool('help')

        # Add custom buttons to toolbar
        self.fig.canvas.manager.toolmanager.add_tool('Show', ShowHideTool, axis=self.axis, graphs=self.graphs)
        self.fig.canvas.manager.toolbar.add_tool('Show', 'navigation', 0)

        # Set Y values
        plt.yticks(np.arange(1, 5))

        # Set X grid
        loc = plticker.MultipleLocator(base=1)
        self.axis.xaxis.set_major_locator(loc)

        # Adjust the bottom and left size according to the
        # requirement of the user
        plt.subplots_adjust(bottom=0.25)
        plt.subplots_adjust(left=0.15)

        plt.grid()

        # Choose the Slider color
        slider_color = 'White'

        # Set the axis and slider position in the plot
        axis_position = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor=slider_color)
        self.slider = Slider(axis_position, 'Pos', 0, 100.0, valinit=0)
        self.slider.valtext.set_visible(False)

        # update graph position 
        self.slider.on_changed(self.update)
        self.update(0)

    # update() function to change the graph when the slider is in use
    def update(self, val):
        # Adjust the slider value to the graphs length
        adjusted_val = val * (self.max_graph_len - self.graph_visible_points) / 100
        self.axis.axis([adjusted_val, adjusted_val + self.graph_visible_points, 0.25, 4.75])
        self.fig.canvas.draw_idle()

    def add_graph(self, x, y, labels):
        if len(labels) != 4:
            raise Exception("Length labels must be 4")

        if not self.allow_float:
            if not issubclass(x.dtype.type, np.integer):
                raise Exception("X values must be integers")

            if not issubclass(y.dtype.type, np.integer):
                raise Exception("Y values must be integers")

        self.graphs[self.graphs_added] = Graph(self.axis, x, y)

        # Resize slider movement to adjust to graph length
        if len(x) > self.max_graph_len:
            self.max_graph_len = len(x)

        line_color = self.graphs[self.graphs_added].get_color()

        if self.graphs_added == 0:
            self.graphs_added = 1

            # Add custom Y-labels
            self.axis.set_yticklabels(labels)

            # Setting up Y-axis tick color
            self.axis.spines['left'].set_color(line_color)

            # Setting up X-axis tick color
            self.axis.tick_params(axis='y', colors=line_color)
        else:
            self.graphs_added = 0

            sec_axis = self.axis.secondary_yaxis(-0.1, functions=(lambda x: x, lambda x: x))

            # Set Y values
            sec_axis.set_yticks(np.arange(1, 5))

            # Add custom Y-labels
            sec_axis.set_yticklabels(labels)

            # setting up Y-axis tick color
            sec_axis.spines['left'].set_color(line_color)

            # setting up X-axis tick color
            sec_axis.tick_params(axis='y', colors=line_color)

    def print_figure(self):
        # Display the plot
        plt.show()

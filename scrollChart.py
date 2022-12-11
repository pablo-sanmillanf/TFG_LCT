# Import libraries using import keyword
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


# Custom Axis to don´t allow Y movement
class My_Axes(matplotlib.axes.Axes):
    name = "My_Axes"
    def drag_pan(self, button, key, x, y):
        matplotlib.axes.Axes.drag_pan(self, button, 'x', x, y) # pretend key=='x'

matplotlib.projections.register_projection(My_Axes)


# Setting Plot and Axis variables as subplots()
# function returns tuple(fig, ax)
Plot, Axis = plt.subplots(subplot_kw={"projection" : "My_Axes"})


# Adjust the bottom size according to the
# requirement of the user
plt.subplots_adjust(bottom=0.25)

# Set the x and y axis to some dummy data
t = np.arange(0.0, 100.0, 0.1)
s = np.sin(np.pi*t/2)

# plot the x and y using plot function
l = plt.plot(t, s, marker="o")

# Choose the Slider color
slider_color = 'White'

# Set the axis and slider position in the plot
axis_position = plt.axes([0.2, 0.1, 0.65, 0.03],
                        facecolor = slider_color)
slider_position = Slider(axis_position,
                        'Pos', 0.1, 90.0)

# update() function to change the graph when the
# slider is in use
def update(val):
    pos = slider_position.val
    Axis.axis([pos, pos+10, -1, 1])
    Plot.canvas.draw_idle()

# update function called using on_changed() function
slider_position.on_changed(update)

# Display the plot
plt.show()
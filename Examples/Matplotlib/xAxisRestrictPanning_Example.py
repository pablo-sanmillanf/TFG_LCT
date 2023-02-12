import matplotlib
import matplotlib.pyplot as plt    

class My_Axes(matplotlib.axes.Axes):
    name = "My_Axes"
    def drag_pan(self, button, key, x, y):
        matplotlib.axes.Axes.drag_pan(self, button, 'x', x, y) # pretend key=='x'

matplotlib.projections.register_projection(My_Axes)

figure = plt.figure()
ax = figure.add_subplot(111, projection="My_Axes")
ax.plot([0, 1, 2], [0, 1, 0])
plt.show()
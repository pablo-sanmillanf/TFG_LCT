# Import libraries using import keyword
import numpy as np
import plotter


# Set the x and y axis to some dummy data
t1 = np.arange(0, 100, 1)
f1 = np.cos(np.pi*t1/2)*1.5 + 2.5

t2 = np.arange(0, 300, 1)
f2 = np.sin(np.pi*t2/2)*1.5 + 2.5

graph = plotter.graph(True)

graph.add_graph(t1, f1, np.array(["SG++", "SG+", "SG-", "SG--"]))
graph.add_graph(t2, f2, np.array(["SD--", "SD-", "SD+", "SD++"]))
graph.print_figure()
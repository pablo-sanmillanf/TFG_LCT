# Import libraries using import keyword
import numpy as np
import plotter
import json

# Read the data
f = open("data.json", "r")

data = json.loads(f.read())


# Set the x and y axis to some dummy data

f1 = np.array(data[0]["data"])
t1 = np.arange(len(f1))

f2 = np.array(data[1]["data"])
t2 = np.arange(len(f2))

plt = plotter.GraphPlotter(False)

plt.add_graph(t1, f1, np.array(data[0]["labels"]))
plt.add_graph(t2, f2, np.array(data[1]["labels"]))
plt.print_figure()
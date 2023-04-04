import sys
import json
import numpy as np
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QWidget,
)

from graph.mpl_canvas import MplWidget


class Window(QWidget):
    def __init__(self):
        super().__init__()

        # Read the data
        f = open("data.json", "r")

        data = json.loads(f.read())

        # Set the x and y-axis to some dummy data
        f1 = np.array(data[0]["data"])
        t1 = np.arange(len(f1))

        f2 = np.array(data[1]["data"])
        t2 = np.arange(len(f2))

        self.mpl = MplWidget()

        self.mpl.add_graph(t1, f1, np.array(data[0]["labels"]))
        self.mpl.add_graph(t2, f2, np.array(data[1]["labels"]))

        hbox = QHBoxLayout(self)
        hbox.addWidget(self.mpl)
        self.setLayout(hbox)


app = QApplication(sys.argv)

w = Window()
w.show()

app.exec()

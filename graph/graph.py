import json
import numpy as np
from PyQt5.QtWidgets import (
    QApplication
)
from graphWindow import Ui_GraphWindow
from PyQt5 import QtWidgets
import sys


class GraphWindow(QtWidgets.QMainWindow, Ui_GraphWindow):

    def __init__(self, *args, **kwargs):
        super(GraphWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.applyStyles()

        # Read the data
        data = json.loads(open("data.json", "r").read())

        # Set the x and y-axis to some dummy data
        f1 = np.array(data[0]["data"])
        t1 = np.arange(len(f1))

        f2 = np.array(data[1]["data"])
        t2 = np.arange(len(f2))

        self.mplWidget.add_graph(t1, f1, np.array(data[0]["labels"]))
        self.mplWidget.add_graph(t2, f2, np.array(data[1]["labels"]))

        # Set slots and signals to move slider and graph at the same time
        self.slider.valueChanged.connect(self.mplWidget.position_changed_slot)
        self.mplWidget.pos_changed.connect(self.slider.setValue)

    def applyStyles(self):
        self.slider.setStyleSheet(open("slider.css", "r").read())


app = QApplication(sys.argv)
main = GraphWindow()
main.show()
sys.exit(app.exec())

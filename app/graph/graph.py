import json
import numpy as np
from PyQt5.QtWidgets import (
    QApplication
)
from .graphWindow import Ui_GraphWindow
from PyQt5 import QtWidgets
import sys


class GraphWindow(QtWidgets.QMainWindow, Ui_GraphWindow):

    def __init__(self, relative_path: str, data, *args, **kwargs):
        super(GraphWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.applyStyles()

        self.relative_path = relative_path

        for f in data:
            y = np.array(f["data"])
            x = np.arange(len(y))
            self.mplWidget.add_graph(x, y, np.array(f["labels"]))

        # Set slots and signals to move slider and graph at the same time
        self.slider.valueChanged.connect(self.mplWidget.position_changed_slot)
        self.mplWidget.pos_changed.connect(self.slider.setValue)

    def applyStyles(self):
        self.slider.setStyleSheet(open(self.relative_path + "slider.css", "r").read())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = GraphWindow("", json.loads(open("./" + "data.json", "r").read()))
    main.show()
    sys.exit(app.exec())

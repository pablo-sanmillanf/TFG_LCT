import json
import numpy as np
from PyQt5.QtWidgets import (
    QApplication
)

from lct_handler import LCTHandler
from .graphWindowQtCreator import Ui_GraphWindow
from PyQt5 import QtWidgets
import sys


class GraphWindow(QtWidgets.QMainWindow, Ui_GraphWindow):

    def __init__(self, relative_path: str, visible_points=10, *args, **kwargs):
        super(GraphWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.relative_path = relative_path
        self.applyStyles()

        self.visible_points = visible_points

        self.clause_data = None
        self.clause_labels = None
        self.mplWidget.point_clicked.connect(self.text.text_selected)

    def update_graphs(self, lct_handler: LCTHandler):
        # Remove previous data
        self.mplWidget.remove_graphs()

        self.clause_data = lct_handler.get_clause_values()
        self.clause_labels = lct_handler.get_clause_labels()

        for i in range(len(self.clause_labels)):
            y = np.array([e[i] for e in self.clause_data])
            x = np.arange(len(y))
            self.mplWidget.add_graph(x, y, np.array(self.clause_labels[i]))

        # Set slots and signals to move slider and graph at the same time
        if self.visible_points < len(self.clause_data):
            self.slider.valueChanged.connect(self.mplWidget.position_changed_slot)
            self.slider.setEnabled(True)
            self.mplWidget.pos_changed.connect(self.slider.setValue)
        else:
            self.slider.setEnabled(False)

        self.text.set_texts(lct_handler.get_super_clause_texts(), lct_handler.get_clause_texts())
        self.text.scroll_updated.connect(lambda pos: self.scrollArea.verticalScrollBar().setValue(pos))

    def applyStyles(self):
        self.slider.setStyleSheet(open(self.relative_path + "slider.css", "r").read())
        self.mplWidget.setStyleSheet("QWidget { border: 0; background: white; margin: 0;}")
        self.text.setStyleSheet(
            "QLabel {"
            "    border: 2px solid green;"
            "    padding: 2px;"
            "    font-size: 16px;"
            "    font-family: 'arial';"
            "    font-weight: bold;"
            "}"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = GraphWindow("", json.loads(open("./" + "data.json", "r").read()))
    main.show()
    sys.exit(app.exec())

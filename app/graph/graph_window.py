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
        self.super_clause_data = None
        self.clause_labels = None
        self.mplWidget.point_clicked.connect(self.text.text_selected)

        self.actiongroupTarget.setExclusive(True)
        self.actionClauses.triggered.connect(lambda x: self.change_target(True))
        self.actionSuperClauses.triggered.connect(lambda x: self.change_target(False))

    def change_target(self, is_normal_clause: bool):
        self.text.set_clauses_type(is_normal_clause)
        if is_normal_clause:
            self._load_data_in_the_graph(self.clause_data)
        else:
            self._load_data_in_the_graph(self.super_clause_data)

    def update_graphs(self, lct_handler: LCTHandler):

        self.clause_data = lct_handler.get_clause_values()
        self.super_clause_data = lct_handler.get_super_clause_values()
        self.clause_labels = lct_handler.get_clause_labels()

        self._load_data_in_the_graph(self.clause_data)

        self.text.set_texts(lct_handler.get_super_clause_texts(), lct_handler.get_clause_texts())
        self.text.scroll_updated.connect(self.scrollArea.verticalScrollBar().setValue)

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

    def _load_data_in_the_graph(self, data: list[list[int]]):
        # Remove previous data
        self.mplWidget.remove_graphs()

        for i in range(len(self.clause_labels)):
            y = np.array([e[i] for e in data])
            x = np.arange(len(y))
            self.mplWidget.add_graph(x, y, np.array(self.clause_labels[i]))

        # Set slots and signals to move slider and graph at the same time
        if self.visible_points < len(data):
            self.slider.valueChanged.connect(self.mplWidget.position_changed_slot)
            self.slider.setEnabled(True)
            self.mplWidget.pos_changed.connect(self.slider.setValue)
        else:
            self.slider.setEnabled(False)

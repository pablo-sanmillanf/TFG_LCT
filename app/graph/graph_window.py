import json
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QInputDialog
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

        self.connected = False

        self.clause_data = None
        self.super_clause_data = None
        self.clause_labels = None
        self.mplWidget.point_clicked.connect(self.text.text_selected)

        self.actiongroupTarget.setExclusive(True)
        self.actionClauses.triggered.connect(lambda x: self.change_target_action(True))
        self.actionSuperClauses.triggered.connect(lambda x: self.change_target_action(False))
        self.actionSD.triggered.connect(lambda x: self.visibility_action(0, x))
        self.actionSG.triggered.connect(lambda x: self.visibility_action(1, x))
        self.actionSave_Visibe_Chart_as_Image.triggered.connect(self.mplWidget.save_figure)
        self.actionVisible_points.triggered.connect(self.set_visible_points_dialog)

    def set_visible_points_dialog(self, s: bool):
        value, ok = QInputDialog().getInt(
            self,
            "Change visible points in the graph",
            "Visible points:",
            self.visible_points,
            1,  # Min value
            50,  # Max value
            1  # Step
        )

        if ok:
            self.visible_points = value
            self.mplWidget.set_visible_points(value)
            self._set_slider_behaviour(len(self.text.get_data()))

    def visibility_action(self, graph_index: int, s: bool):
        self.mplWidget.set_graph_visible(graph_index, s)

    def change_target_action(self, is_normal_clause: bool):
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

        self._set_slider_behaviour(len(data))

    def _set_slider_behaviour(self, data_len):
        self.slider.setValue(0)
        # Set slots and signals to move slider and graph at the same time
        if self.visible_points < data_len:
            self.slider.setEnabled(True)
            if not self.connected:
                self.connected = True
                self.slider.valueChanged.connect(self.mplWidget.position_changed_slot)
                self.mplWidget.pos_changed.connect(self.slider.setValue)
        else:
            self.slider.setEnabled(False)
            if self.connected:
                self.connected = False
                self.slider.valueChanged.disconnect(self.mplWidget.position_changed_slot)
                self.mplWidget.pos_changed.disconnect(self.slider.setValue)

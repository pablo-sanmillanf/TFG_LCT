import numpy as np
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtWidgets import (
    QInputDialog, QFileDialog
)

from ..lct_handler import LCTHandler
from .graphWindowQtCreator import Ui_GraphWindow
from PyQt5 import QtWidgets, QtGui

from .graph_resources import graph_resources
from ..main_resources import main_resources

TEXT_SG = "SG"
TEXT_SD = "SD"


class GraphWindow(QtWidgets.QMainWindow, Ui_GraphWindow):
    """
    Manages the window used to represent the results of the analysis of the text in a graph.
    There should be one object of this class and call update_graphs() function every time an update of the plotted data
    is needed.
    """

    def __init__(self, relative_path: str, visible_points: int = 10, *args, **kwargs) -> None:
        """
        Object creation.
        :param relative_path: Path that will be taken as root directory for this module.
        :param visible_points: Visible x-points in the graph.
        :param args:
        :param kwargs:
        """
        super(GraphWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self._relative_path = relative_path
        self._apply_styles()

        self.setWindowIcon(QtGui.QIcon(':/icon/logo'))

        self._visible_points = visible_points

        self._connected = False

        self._clause_data = None
        self._super_clause_data = None
        self._clause_labels = None
        self.mplWidget.point_clicked.connect(self.text.text_selected)

        self.actiongroupTarget.setExclusive(True)
        self.actionClauses.triggered.connect(lambda x: self._change_target_action(True))
        self.actionSuperClauses.triggered.connect(lambda x: self._change_target_action(False))
        self.actionSD.triggered.connect(self._sd_visibility_action)
        self.actionSG.triggered.connect(self._sg_visibility_action)
        self.actionSave_Visibe_Chart_as_Image.triggered.connect(self._save_figure)
        self.actionVisible_points.triggered.connect(self._set_visible_points_dialog)

    def _save_figure(self, s: bool) -> None:
        """
        Show a dialog to select the path where the image of the graph will be saved.
        :param s: The value of the button. Non-relevant.
        """
        file, file_type = QFileDialog().getSaveFileName(
            self,
            "Save graph as image",
            self._relative_path,
            "Images (*.png *.jpg)"
        )
        if file != "":
            self.mplWidget.save_figure(file)

    def _set_visible_points_dialog(self, s: bool) -> None:
        """
        Show a dialog to select the visible x-points in the graph. If the number of visible points is grater than the
        number of points of the functions, the slider will be disabled.
        :param s: The value of the button. Non-relevant.
        """
        value, ok = QInputDialog().getInt(
            self,
            "Change visible points in the graph",
            "Visible points:",
            self._visible_points,
            1,  # Min value
            50,  # Max value
            1  # Step
        )

        if ok:
            self._visible_points = value
            self.mplWidget.set_visible_points(value)
            self._set_slider_behaviour(len(self.text.get_data()))

    def _sd_visibility_action(self, s: bool) -> None:
        """
        Set the visibility of the SD function depending on the s state.
        :param s: The state of the button.
        """
        self.mplWidget.set_graph_visible(0, s)

    def _sg_visibility_action(self, s: bool) -> None:
        """
        Set the visibility of the SG function depending on the s state. This function take into account if the target is
        SG alone or together with SD.
        :param s: The state of the button.
        """
        if self.actionSD.isEnabled():
            self.mplWidget.set_graph_visible(1, s)
        else:
            self.mplWidget.set_graph_visible(0, s)

    def _change_target_action(self, is_normal_clause: bool) -> None:
        """
        Select the visible functions in the graph from clauses or super clauses depending on is_normal_clause parameter.
        :param is_normal_clause: True if is clauses, False if is super clauses.
        """
        self.text.set_clauses_type(is_normal_clause)
        if is_normal_clause:
            self._load_data_in_the_graph(self._clause_data)
        else:
            self._load_data_in_the_graph(self._super_clause_data)

    def update_graphs(self, lct_handler: LCTHandler) -> None:
        """
        Update the info showed in the graph and the data for the clauses and super clauses and the associated target.
        :param lct_handler: The object with the analyzed texts to be represented.
        """

        self._clause_data = lct_handler.get_clause_values()
        self._super_clause_data = lct_handler.get_super_clause_values()
        self._clause_labels = lct_handler.get_clause_labels()

        self._load_data_in_the_graph(self._clause_data)

        raw_labels = lct_handler.get_raw_labels()

        if raw_labels[0] in TEXT_SG:
            self.actionSD.setEnabled(False)
            self.actionSD.setChecked(False)
            self.actionSG.setEnabled(True)
            self.actionSG.setChecked(True)
        elif raw_labels[0] in TEXT_SD:
            if len(raw_labels) == 1:
                self.actionSD.setEnabled(True)
                self.actionSD.setChecked(True)
                self.actionSG.setEnabled(False)
                self.actionSG.setChecked(False)
            elif len(raw_labels) == 2 and raw_labels[1] in TEXT_SG:
                self.actionSD.setEnabled(True)
                self.actionSD.setChecked(True)
                self.actionSG.setEnabled(True)
                self.actionSG.setChecked(True)
            else:
                self.actionSD.setEnabled(False)
                self.actionSD.setChecked(False)
                self.actionSG.setEnabled(False)
                self.actionSG.setChecked(False)
        else:
            self.actionSD.setEnabled(False)
            self.actionSD.setChecked(False)
            self.actionSG.setEnabled(False)
            self.actionSG.setChecked(False)

        self.actionClauses.setChecked(True)

        self.text.set_texts(lct_handler.get_super_clause_texts(), lct_handler.get_clause_texts())
        self.text.scroll_updated.connect(self.scrollArea.verticalScrollBar().setValue)

    def _apply_styles(self) -> None:
        """
        Apply CSS styles to the widgets in the window.
        """
        file = QFile(":/styles/slider")
        file.open(QFile.ReadOnly)
        self.slider.setStyleSheet(QTextStream(file.readAll()).readAll())
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

    def _load_data_in_the_graph(self, data: list[list[int]]) -> None:
        """
        Remove the previous data and load the new data in the graph.
        :param data: The data as several list of integers that represents the y-values.
        """
        # Remove previous data
        self.mplWidget.remove_graphs()

        for i in range(len(self._clause_labels)):
            y = np.array([e[i] for e in data])
            x = np.arange(len(y))
            self.mplWidget.add_graph(x, y, np.array(self._clause_labels[i]))

        self._set_slider_behaviour(len(data))

    def _set_slider_behaviour(self, data_len: int) -> None:
        """
        Enable or disable the slider and its associated signals and slots depending on the data_len. If data_len is
        greater than the _visible_points attribute, the slider is enabled and moves solidarity with the graph panning.
        If not, the slider is set to position 0 and disabled.
        :param data_len: The length of the data represented in the graph.
        """
        self.slider.setValue(0)
        # Set slots and signals to move slider and graph at the same time
        if self._visible_points < data_len:
            self.slider.setEnabled(True)
            if not self._connected:
                self._connected = True
                self.slider.valueChanged.connect(self.mplWidget.position_changed_slot)
                self.mplWidget.pos_changed.connect(self.slider.setValue)
        else:
            self.slider.setEnabled(False)
            if self._connected:
                self._connected = False
                self.slider.valueChanged.disconnect(self.mplWidget.position_changed_slot)
                self.mplWidget.pos_changed.disconnect(self.slider.setValue)

import json
import sys

from PyQt5 import QtGui
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow, QInputDialog, QMessageBox, QFileDialog
)

from dialogs.colors_dialog import ColorsDialog
from graph.graph_window import GraphWindow
from mainWindowQtCreator import Ui_MainWindow


def manage_file(file: str, operation: str, data: str = None) -> str:
    result = None
    f = None
    try:
        f = open(file, operation, encoding="utf8")
        if operation == "r":
            result = f.read()
        elif operation == "w":
            f.write(data)
    finally:
        f.close()
    return result


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.graph_window = None

        self.conf = json.loads(manage_file("defaultconf.json", "r"))

        self.conf_has_changed = False

        self.classifierView.setup(
            10,
            10,
            500,
            500,
            "This is an example text. If you want to start editing a file select \"File\"->\"Open...\" and browse to "
            "desired file.\nTo set a division in the text, right-click and select \"Split\". To undo a division in the "
            "text, right-click and select \"Join\" near the splitter.",
            self.conf["text_size"],
            "SD~;SG~",
            list(self.conf["colors"]["together"].values())
        )

        self.actionOpen.triggered.connect(self.open_file_dialog)
        self.actionText_size.triggered.connect(self.text_size_dialog)
        self.actionRects_colors.triggered.connect(self.rects_colors_dialog)
        self.actionSD.triggered.connect(lambda checked: self.target_action("SD~"))
        self.actionSG.triggered.connect(lambda checked: self.target_action("SG~"))
        self.actionSD_SG.triggered.connect(lambda checked: self.target_action("SD~;SG~"))
        self.actiongroupTarget.setExclusive(True)
        self.actionRun_Plotter.triggered.connect(self.run_graph_window)

    def open_file_dialog(self, s: bool) -> None:
        file, file_type = QFileDialog().getOpenFileName(
            self,
            "Open file to analyze",
            "./",
            "Text files (*.txt)"
        )
        if file != "":
            text = manage_file(file, "r")
            if text is None or text == "":
                QMessageBox.critical(self, "File Error", "The selected file has not valid content", QMessageBox.Ok)
                self.open_file_dialog(True)
            else:
                self.classifierView.set_text(text)

    def text_size_dialog(self, s: bool) -> None:
        value, ok = QInputDialog().getInt(
            self,
            "Change text size",
            "Text size:",
            self.classifierView.get_text_size(),
            4,  # Min value
            30,  # Max value
            1  # Step
        )

        if ok:
            self.classifierView.set_text_size(value)
            self.conf["text_size"] = value
            self.conf_has_changed = True

    def rects_colors_dialog(self, s: bool) -> None:
        dlg = ColorsDialog(self.conf["colors"], self)
        dlg.exec()

        if dlg.has_changed:
            self.conf["colors"] = dlg.colors
            if self.classifierView.get_default_descriptor() == "SD~;SG~":
                self.classifierView.set_colors(list(self.conf["colors"]["together"].values()))
            else:
                self.classifierView.set_colors(list(self.conf["colors"]["alone"].values()))
            self.conf_has_changed = True

    def target_action(self, text: str) -> None:
        if text != self.classifierView.get_default_descriptor():
            if text == "SD~;SG~":
                self.classifierView.set_default_descriptor(text, list(self.conf["colors"]["together"].values()))
            else:
                self.classifierView.set_default_descriptor(text, list(self.conf["colors"]["alone"].values()))

    def run_graph_window(self, s: bool) -> None:
        if self.graph_window is None:
            self.graph_window = GraphWindow("graph/")
        self.graph_window.show()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self.conf_has_changed:
            button = QMessageBox.question(self, "Save settings", "Save current settings as default?")
            if button == QMessageBox.Yes:
                manage_file("defaultconf.json", "w", json.dumps(self.conf))
        super().closeEvent(a0)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    w = MainWindow()
    w.show()

    app.exec()

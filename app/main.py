import json
import sys
import re

from PyQt5 import QtGui
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow, QInputDialog, QDialog, QPushButton, QColorDialog, QMessageBox, QFileDialog, QAction

)

from graph.graph import GraphWindow
from colorsDialog import Ui_ColorsDialog
from mainWindow import Ui_MainWindow


def get_btn_style_str(color: str) -> str:
    return (
            "QPushButton {"
            "    border: 2px solid \"grey\";"
            "    background-color: \"" + color + "\";"
            "    min-height: 20px;"
            "    margin-top: 5px;"
            "}"
    )


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


class ColorsDialog(QDialog, Ui_ColorsDialog):
    def __init__(self, colors, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.colors = colors
        self.has_changed = False

        self.set_button_styles()
        self.set_button_actions()

    def set_button_actions(self) -> None:
        # Set alone-tab button actions
        self.alone_default_button.clicked.connect(
            lambda checked: self.button_clicked_dialog(self.alone_default_button)
        )
        self.alone_d_plusplus_button.clicked.connect(
            lambda checked: self.button_clicked_dialog(self.alone_d_plusplus_button)
        )
        self.alone_d_plus_button.clicked.connect(
            lambda checked: self.button_clicked_dialog(self.alone_d_plus_button)
        )
        self.alone_d_minus_button.clicked.connect(
            lambda checked: self.button_clicked_dialog(self.alone_d_minus_button)
        )
        self.alone_d_minusminus_button.clicked.connect(
            lambda checked: self.button_clicked_dialog(self.alone_d_minusminus_button)
        )

        # Set together-tab button actions
        self.together_default_button.clicked.connect(
            lambda checked: self.button_clicked_dialog(self.together_default_button)
        )
        self.together_d_plusplus_g_minusminus_button.clicked.connect(
            lambda checked: self.button_clicked_dialog(self.together_d_plusplus_g_minusminus_button)
        )
        self.together_d_plusplus_g_minus_button.clicked.connect(
            lambda checked: self.button_clicked_dialog(self.together_d_plusplus_g_minus_button)
        )
        self.together_d_plusplus_g_plus_button.clicked.connect(
            lambda checked: self.button_clicked_dialog(self.together_d_plusplus_g_plus_button)
        )
        self.together_d_plusplus_g_plusplus_button.clicked.connect(
            lambda checked: self.button_clicked_dialog(self.together_d_plusplus_g_plusplus_button)
        )
        self.together_d_plus_g_minusminus_button.clicked.connect(
            lambda checked: self.button_clicked_dialog(self.together_d_plus_g_minusminus_button)
        )
        self.together_d_plus_g_minus_button.clicked.connect(
            lambda checked: self.button_clicked_dialog(self.together_d_plus_g_minus_button)
        )
        self.together_d_plus_g_plus_button.clicked.connect(
            lambda checked: self.button_clicked_dialog(self.together_d_plus_g_plus_button)
        )
        self.together_d_plus_g_plusplus_button.clicked.connect(
            lambda checked: self.button_clicked_dialog(self.together_d_plus_g_plusplus_button)
        )
        self.together_d_minus_g_minusminus_button.clicked.connect(
            lambda checked: self.button_clicked_dialog(self.together_d_minus_g_minusminus_button)
        )
        self.together_d_minus_g_minus_button.clicked.connect(
            lambda checked: self.button_clicked_dialog(self.together_d_minus_g_minus_button)
        )
        self.together_d_minus_g_plus_button.clicked.connect(
            lambda checked: self.button_clicked_dialog(self.together_d_minus_g_plus_button)
        )
        self.together_d_minus_g_plusplus_button.clicked.connect(
            lambda checked: self.button_clicked_dialog(self.together_d_minus_g_plusplus_button)
        )
        self.together_d_minusminus_g_minusminus_button.clicked.connect(
            lambda checked: self.button_clicked_dialog(self.together_d_minusminus_g_minusminus_button)
        )
        self.together_d_minusminus_g_minus_button.clicked.connect(
            lambda checked: self.button_clicked_dialog(self.together_d_minusminus_g_minus_button)
        )
        self.together_d_minusminus_g_plus_button.clicked.connect(
            lambda checked: self.button_clicked_dialog(self.together_d_minusminus_g_plus_button)
        )
        self.together_d_minusminus_g_plusplus_button.clicked.connect(
            lambda checked: self.button_clicked_dialog(self.together_d_minusminus_g_plusplus_button)
        )

    def set_button_styles(self) -> None:

        # Set alone-tab button styles
        self.alone_default_button.setStyleSheet(get_btn_style_str(self.colors["alone"]["Default"]))
        self.alone_d_plusplus_button.setStyleSheet(get_btn_style_str(self.colors["alone"]["SD++"]))
        self.alone_d_plus_button.setStyleSheet(get_btn_style_str(self.colors["alone"]["SD+"]))
        self.alone_d_minus_button.setStyleSheet(get_btn_style_str(self.colors["alone"]["SD-"]))
        self.alone_d_minusminus_button.setStyleSheet(get_btn_style_str(self.colors["alone"]["SD--"]))

        # Set together-tab button styles
        self.together_default_button.setStyleSheet(
            get_btn_style_str(self.colors["together"]["Default"])
        )
        self.together_d_plusplus_g_minusminus_button.setStyleSheet(
            get_btn_style_str(self.colors["together"]["SD++;SG--"])
        )
        self.together_d_plusplus_g_minus_button.setStyleSheet(
            get_btn_style_str(self.colors["together"]["SD++;SG-"])
        )
        self.together_d_plusplus_g_plus_button.setStyleSheet(
            get_btn_style_str(self.colors["together"]["SD++;SG+"])
        )
        self.together_d_plusplus_g_plusplus_button.setStyleSheet(
            get_btn_style_str(self.colors["together"]["SD++;SG++"])
        )
        self.together_d_plus_g_minusminus_button.setStyleSheet(
            get_btn_style_str(self.colors["together"]["SD+;SG--"])
        )
        self.together_d_plus_g_minus_button.setStyleSheet(
            get_btn_style_str(self.colors["together"]["SD+;SG-"])
        )
        self.together_d_plus_g_plus_button.setStyleSheet(
            get_btn_style_str(self.colors["together"]["SD+;SG+"])
        )
        self.together_d_plus_g_plusplus_button.setStyleSheet(
            get_btn_style_str(self.colors["together"]["SD+;SG++"])
        )
        self.together_d_minus_g_minusminus_button.setStyleSheet(
            get_btn_style_str(self.colors["together"]["SD-;SG--"])
        )
        self.together_d_minus_g_minus_button.setStyleSheet(
            get_btn_style_str(self.colors["together"]["SD-;SG-"])
        )
        self.together_d_minus_g_plus_button.setStyleSheet(
            get_btn_style_str(self.colors["together"]["SD-;SG+"])
        )
        self.together_d_minus_g_plusplus_button.setStyleSheet(
            get_btn_style_str(self.colors["together"]["SD-;SG++"])
        )
        self.together_d_minusminus_g_minusminus_button.setStyleSheet(
            get_btn_style_str(self.colors["together"]["SD--;SG--"])
        )
        self.together_d_minusminus_g_minus_button.setStyleSheet(
            get_btn_style_str(self.colors["together"]["SD--;SG-"])
        )
        self.together_d_minusminus_g_plus_button.setStyleSheet(
            get_btn_style_str(self.colors["together"]["SD--;SG+"])
        )
        self.together_d_minusminus_g_plusplus_button.setStyleSheet(
            get_btn_style_str(self.colors["together"]["SD--;SG++"])
        )

    def button_clicked_dialog(self, button: QPushButton) -> None:
        new_color = QColorDialog().getColor(
            QColor(re.search("background-color: \"([#a-zA-Z0-9]*)\";", button.styleSheet()).group(1)),
            self,
            "Change color"
        )

        if new_color.isValid():
            button.setStyleSheet(get_btn_style_str(new_color.name()))
            self.has_changed = True
            match button:
                case self.alone_default_button:
                    self.colors["alone"]["Default"] = new_color.name()
                case self.alone_d_plusplus_button:
                    self.colors["alone"]["SD++"] = new_color.name()
                case self.alone_d_plus_button:
                    self.colors["alone"]["SD+"] = new_color.name()
                case self.alone_d_minus_button:
                    self.colors["alone"]["SD-"] = new_color.name()
                case self.alone_d_minusminus_button:
                    self.colors["alone"]["SD--"] = new_color.name()
                case self.together_default_button:
                    self.colors["together"]["Default"] = new_color.name()
                case self.together_d_plusplus_g_minusminus_button:
                    self.colors["together"]["SD++;SG--"] = new_color.name()
                case self.together_d_plusplus_g_minus_button:
                    self.colors["together"]["SD++;SG-"] = new_color.name()
                case self.together_d_plusplus_g_plus_button:
                    self.colors["together"]["SD++;SG+"] = new_color.name()
                case self.together_d_plusplus_g_plusplus_button:
                    self.colors["together"]["SD++;SG++"] = new_color.name()
                case self.together_d_plus_g_minusminus_button:
                    self.colors["together"]["SD+;SG--"] = new_color.name()
                case self.together_d_plus_g_minus_button:
                    self.colors["together"]["SD+;SG-"] = new_color.name()
                case self.together_d_plus_g_plus_button:
                    self.colors["together"]["SD+;SG+"] = new_color.name()
                case self.together_d_plus_g_plusplus_button:
                    self.colors["together"]["SD+;SG++"] = new_color.name()
                case self.together_d_minus_g_minusminus_button:
                    self.colors["together"]["SD-;SG--"] = new_color.name()
                case self.together_d_minus_g_minus_button:
                    self.colors["together"]["SD-;SG-"] = new_color.name()
                case self.together_d_minus_g_plus_button:
                    self.colors["together"]["SD-;SG+"] = new_color.name()
                case self.together_d_minus_g_plusplus_button:
                    self.colors["together"]["SD-;SG++"] = new_color.name()
                case self.together_d_minusminus_g_minusminus_button:
                    self.colors["together"]["SD--;SG--"] = new_color.name()
                case self.together_d_minusminus_g_minus_button:
                    self.colors["together"]["SD--;SG-"] = new_color.name()
                case self.together_d_minusminus_g_plus_button:
                    self.colors["together"]["SD--;SG+"] = new_color.name()
                case self.together_d_minusminus_g_plusplus_button:
                    self.colors["together"]["SD--;SG++"] = new_color.name()
                case _:
                    print("ERROR")


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.graph_window = None

        self.conf = json.loads(manage_file("defaultconf.json", "r"))

        self.conf_has_changed = False

        self.textHandler.setup(
            10,
            10,
            500,
            500,
            "This is an example text. If you want to start editing a file select \"File\"->\"Open...\" and browse to "
            "desired file. To set a division in the text, right-click and select \"Split\". To undo a division in the "
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
                self.textHandler.set_text(text)

    def text_size_dialog(self, s: bool) -> None:
        value, ok = QInputDialog().getInt(
            self,
            "Change text size",
            "Text size:",
            self.textHandler.get_text_size(),
            4,  # Min value
            30,  # Max value
            1  # Step
        )

        if ok:
            self.textHandler.set_text_size(value)
            self.conf["text_size"] = value
            self.conf_has_changed = True

    def rects_colors_dialog(self, s: bool) -> None:
        dlg = ColorsDialog(self.conf["colors"], self)
        dlg.exec()

        if dlg.has_changed:
            self.conf["colors"] = dlg.colors
            if self.textHandler.get_default_descriptor() == "SD~;SG~":
                self.textHandler.set_colors(list(self.conf["colors"]["together"].values()))
            else:
                self.textHandler.set_colors(list(self.conf["colors"]["alone"].values()))
            self.conf_has_changed = True

    def target_action(self, text: str) -> None:
        if text != self.textHandler.get_default_descriptor():
            if text == "SD~;SG~":
                self.textHandler.set_default_descriptor(text, list(self.conf["colors"]["together"].values()))
            else:
                self.textHandler.set_default_descriptor(text, list(self.conf["colors"]["alone"].values()))

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

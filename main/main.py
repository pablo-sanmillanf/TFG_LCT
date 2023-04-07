import json
import sys
import re

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow, QInputDialog, QDialog, QPushButton, QColorDialog

)

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


class ColorsDialog(QDialog, Ui_ColorsDialog):
    def __init__(self, colors, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.set_button_styles(colors)

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

    def set_button_styles(self, colors) -> None:

        # Set alone-tab button styles
        self.alone_default_button.setStyleSheet(get_btn_style_str(colors["alone"]["Default"]))
        self.alone_d_plusplus_button.setStyleSheet(get_btn_style_str(colors["alone"]["SD++"]))
        self.alone_d_plus_button.setStyleSheet(get_btn_style_str(colors["alone"]["SD+"]))
        self.alone_d_minus_button.setStyleSheet(get_btn_style_str(colors["alone"]["SD-"]))
        self.alone_d_minusminus_button.setStyleSheet(get_btn_style_str(colors["alone"]["SD--"]))

        # Set together-tab button styles
        self.together_default_button.setStyleSheet(get_btn_style_str(colors["together"]["Default"]))
        self.together_d_plusplus_g_minusminus_button.setStyleSheet(get_btn_style_str(colors["together"]["SD++;SG--"]))
        self.together_d_plusplus_g_minus_button.setStyleSheet(get_btn_style_str(colors["together"]["SD++;SG-"]))
        self.together_d_plusplus_g_plus_button.setStyleSheet(get_btn_style_str(colors["together"]["SD++;SG+"]))
        self.together_d_plusplus_g_plusplus_button.setStyleSheet(get_btn_style_str(colors["together"]["SD++;SG++"]))
        self.together_d_plus_g_minusminus_button.setStyleSheet(get_btn_style_str(colors["together"]["SD+;SG--"]))
        self.together_d_plus_g_minus_button.setStyleSheet(get_btn_style_str(colors["together"]["SD+;SG-"]))
        self.together_d_plus_g_plus_button.setStyleSheet(get_btn_style_str(colors["together"]["SD+;SG+"]))
        self.together_d_plus_g_plusplus_button.setStyleSheet(get_btn_style_str(colors["together"]["SD+;SG++"]))
        self.together_d_minus_g_minusminus_button.setStyleSheet(get_btn_style_str(colors["together"]["SD-;SG--"]))
        self.together_d_minus_g_minus_button.setStyleSheet(get_btn_style_str(colors["together"]["SD-;SG-"]))
        self.together_d_minus_g_plus_button.setStyleSheet(get_btn_style_str(colors["together"]["SD-;SG+"]))
        self.together_d_minus_g_plusplus_button.setStyleSheet(get_btn_style_str(colors["together"]["SD-;SG++"]))
        self.together_d_minusminus_g_minusminus_button.setStyleSheet(get_btn_style_str(colors["together"]["SD--;SG--"]))
        self.together_d_minusminus_g_minus_button.setStyleSheet(get_btn_style_str(colors["together"]["SD--;SG-"]))
        self.together_d_minusminus_g_plus_button.setStyleSheet(get_btn_style_str(colors["together"]["SD--;SG+"]))
        self.together_d_minusminus_g_plusplus_button.setStyleSheet(get_btn_style_str(colors["together"]["SD--;SG++"]))

    def button_clicked_dialog(self, button: QPushButton) -> None:
        new_color = QColorDialog().getColor(
            QColor(re.search("background-color: \"([#a-zA-Z0-9]*)\";", button.styleSheet()).group(1)),
            self,
            "Change color"
        )

        if new_color.isValid():
            button.setStyleSheet(get_btn_style_str(new_color.name()))


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.default_conf = json.loads(open("defaultconf.json", "r").read())

        self.textHandler.setup(
            10,
            10,
            500,
            500,
            open("text.txt", "r").read(),
            13,
            "SD~;SG~",
            list(self.default_conf["colors"]["together"].values())
        )

        self.actionText_size.triggered.connect(self.text_size_dialog)
        self.actionRects_colors.triggered.connect(self.rects_colors_dialog)

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

    def rects_colors_dialog(self, s: bool) -> None:
        dlg = ColorsDialog(self.default_conf["colors"], self)
        dlg.exec()


app = QApplication(sys.argv)

w = MainWindow()
w.show()

app.exec()

import re

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QDialog, QColorDialog, QPushButton

from .colorsDialogQtCreator import Ui_ColorsDialog


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
                    raise RuntimeError("ERROR")

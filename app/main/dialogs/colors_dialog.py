import re

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QDialog, QColorDialog, QPushButton

from .colorsDialogQtCreator import Ui_ColorsDialog


def _get_btn_style_str(color: str) -> str:
    """
    This function helps to set the CSS style of the buttons of the dialog. All the CSS properties are the same  for all
    the buttons except the color, that is passed as a parameter.
    :param color: The color of the CSS-style. Should be a valid CSS color.
    :return: The style of the button.
    """
    return (
            "QPushButton {"
            "    border: 2px solid \"grey\";"
            "    background-color: \"" + color + "\";"
            "    min-height: 20px;"
            "    margin-top: 5px;"
            "}"
    )


class ColorsDialog(QDialog, Ui_ColorsDialog):
    """
    This class manages the change of all the colors for the targets SD, SG and SG and SG together.
    The dialog has two tabs: one called alone to edit the background color when the target is SD or SG alone, and
    another called together to edit the background color when the target is SD and SG together. To edit a color from a
    specific value, the user has to click the associated button and a Color Dialog will be shown to find the desired
    color.
    """
    def __init__(self, colors, parent=None):
        """

        :param colors: A dictionary with all the colors that will be able to edit in the dialog.
        :param parent: The QWidget that calls this dialog.
        """
        super().__init__(parent)
        self.setupUi(self)

        self.colors = colors
        self.has_changed = False

        self._set_button_styles()
        self._set_button_actions()

    def _set_button_actions(self) -> None:
        """
        Connect the clicked signal for all the buttons with the slot "_button_clicked_dialog()" that will show a
        QColorDialog that will change the background-color of the button and the SG/SD/SG;SD associated value.
        """
        # Set alone-tab button actions
        self._alone_default_button.clicked.connect(
            lambda checked: self._button_clicked_dialog(self._alone_default_button)
        )
        self._alone_d_plusplus_button.clicked.connect(
            lambda checked: self._button_clicked_dialog(self._alone_d_plusplus_button)
        )
        self._alone_d_plus_button.clicked.connect(
            lambda checked: self._button_clicked_dialog(self._alone_d_plus_button)
        )
        self._alone_d_minus_button.clicked.connect(
            lambda checked: self._button_clicked_dialog(self._alone_d_minus_button)
        )
        self._alone_d_minusminus_button.clicked.connect(
            lambda checked: self._button_clicked_dialog(self._alone_d_minusminus_button)
        )

        # Set together-tab button actions
        self._together_default_button.clicked.connect(
            lambda checked: self._button_clicked_dialog(self._together_default_button)
        )
        self._together_d_plusplus_g_minusminus_button.clicked.connect(
            lambda checked: self._button_clicked_dialog(self._together_d_plusplus_g_minusminus_button)
        )
        self._together_d_plusplus_g_minus_button.clicked.connect(
            lambda checked: self._button_clicked_dialog(self._together_d_plusplus_g_minus_button)
        )
        self._together_d_plusplus_g_plus_button.clicked.connect(
            lambda checked: self._button_clicked_dialog(self._together_d_plusplus_g_plus_button)
        )
        self._together_d_plusplus_g_plusplus_button.clicked.connect(
            lambda checked: self._button_clicked_dialog(self._together_d_plusplus_g_plusplus_button)
        )
        self._together_d_plus_g_minusminus_button.clicked.connect(
            lambda checked: self._button_clicked_dialog(self._together_d_plus_g_minusminus_button)
        )
        self._together_d_plus_g_minus_button.clicked.connect(
            lambda checked: self._button_clicked_dialog(self._together_d_plus_g_minus_button)
        )
        self._together_d_plus_g_plus_button.clicked.connect(
            lambda checked: self._button_clicked_dialog(self._together_d_plus_g_plus_button)
        )
        self._together_d_plus_g_plusplus_button.clicked.connect(
            lambda checked: self._button_clicked_dialog(self._together_d_plus_g_plusplus_button)
        )
        self._together_d_minus_g_minusminus_button.clicked.connect(
            lambda checked: self._button_clicked_dialog(self._together_d_minus_g_minusminus_button)
        )
        self._together_d_minus_g_minus_button.clicked.connect(
            lambda checked: self._button_clicked_dialog(self._together_d_minus_g_minus_button)
        )
        self._together_d_minus_g_plus_button.clicked.connect(
            lambda checked: self._button_clicked_dialog(self._together_d_minus_g_plus_button)
        )
        self._together_d_minus_g_plusplus_button.clicked.connect(
            lambda checked: self._button_clicked_dialog(self._together_d_minus_g_plusplus_button)
        )
        self._together_d_minusminus_g_minusminus_button.clicked.connect(
            lambda checked: self._button_clicked_dialog(self._together_d_minusminus_g_minusminus_button)
        )
        self._together_d_minusminus_g_minus_button.clicked.connect(
            lambda checked: self._button_clicked_dialog(self._together_d_minusminus_g_minus_button)
        )
        self._together_d_minusminus_g_plus_button.clicked.connect(
            lambda checked: self._button_clicked_dialog(self._together_d_minusminus_g_plus_button)
        )
        self._together_d_minusminus_g_plusplus_button.clicked.connect(
            lambda checked: self._button_clicked_dialog(self._together_d_minusminus_g_plusplus_button)
        )

    def _set_button_styles(self) -> None:
        """
        Apply the style for all the buttons of the dialog.
        """

        # Set alone-tab button styles
        self._alone_default_button.setStyleSheet(_get_btn_style_str(self.colors["alone"]["Default"]))
        self._alone_d_plusplus_button.setStyleSheet(_get_btn_style_str(self.colors["alone"]["SD++"]))
        self._alone_d_plus_button.setStyleSheet(_get_btn_style_str(self.colors["alone"]["SD+"]))
        self._alone_d_minus_button.setStyleSheet(_get_btn_style_str(self.colors["alone"]["SD-"]))
        self._alone_d_minusminus_button.setStyleSheet(_get_btn_style_str(self.colors["alone"]["SD--"]))

        # Set together-tab button styles
        self._together_default_button.setStyleSheet(
            _get_btn_style_str(self.colors["together"]["Default"])
        )
        self._together_d_plusplus_g_minusminus_button.setStyleSheet(
            _get_btn_style_str(self.colors["together"]["SD++;SG--"])
        )
        self._together_d_plusplus_g_minus_button.setStyleSheet(
            _get_btn_style_str(self.colors["together"]["SD++;SG-"])
        )
        self._together_d_plusplus_g_plus_button.setStyleSheet(
            _get_btn_style_str(self.colors["together"]["SD++;SG+"])
        )
        self._together_d_plusplus_g_plusplus_button.setStyleSheet(
            _get_btn_style_str(self.colors["together"]["SD++;SG++"])
        )
        self._together_d_plus_g_minusminus_button.setStyleSheet(
            _get_btn_style_str(self.colors["together"]["SD+;SG--"])
        )
        self._together_d_plus_g_minus_button.setStyleSheet(
            _get_btn_style_str(self.colors["together"]["SD+;SG-"])
        )
        self._together_d_plus_g_plus_button.setStyleSheet(
            _get_btn_style_str(self.colors["together"]["SD+;SG+"])
        )
        self._together_d_plus_g_plusplus_button.setStyleSheet(
            _get_btn_style_str(self.colors["together"]["SD+;SG++"])
        )
        self._together_d_minus_g_minusminus_button.setStyleSheet(
            _get_btn_style_str(self.colors["together"]["SD-;SG--"])
        )
        self._together_d_minus_g_minus_button.setStyleSheet(
            _get_btn_style_str(self.colors["together"]["SD-;SG-"])
        )
        self._together_d_minus_g_plus_button.setStyleSheet(
            _get_btn_style_str(self.colors["together"]["SD-;SG+"])
        )
        self._together_d_minus_g_plusplus_button.setStyleSheet(
            _get_btn_style_str(self.colors["together"]["SD-;SG++"])
        )
        self._together_d_minusminus_g_minusminus_button.setStyleSheet(
            _get_btn_style_str(self.colors["together"]["SD--;SG--"])
        )
        self._together_d_minusminus_g_minus_button.setStyleSheet(
            _get_btn_style_str(self.colors["together"]["SD--;SG-"])
        )
        self._together_d_minusminus_g_plus_button.setStyleSheet(
            _get_btn_style_str(self.colors["together"]["SD--;SG+"])
        )
        self._together_d_minusminus_g_plusplus_button.setStyleSheet(
            _get_btn_style_str(self.colors["together"]["SD--;SG++"])
        )

    def _button_clicked_dialog(self, button: QPushButton) -> None:
        """
        Manages the QColorDialog associated to the QPushButton and changes the background-color of this button and its
        associated SG/SD/SG;SD value in the color dict.
        :param button: The QPushButton that has been clicked.
        """
        new_color = QColorDialog().getColor(
            QColor(re.search("background-color: \"([#a-zA-Z0-9]*)\";", button.styleSheet()).group(1)),
            self,
            "Change color"
        )

        if new_color.isValid():
            button.setStyleSheet(_get_btn_style_str(new_color.name()))
            self.has_changed = True
            match button:
                case self._alone_default_button:
                    self.colors["alone"]["Default"] = new_color.name()
                case self._alone_d_plusplus_button:
                    self.colors["alone"]["SD++"] = new_color.name()
                case self._alone_d_plus_button:
                    self.colors["alone"]["SD+"] = new_color.name()
                case self._alone_d_minus_button:
                    self.colors["alone"]["SD-"] = new_color.name()
                case self._alone_d_minusminus_button:
                    self.colors["alone"]["SD--"] = new_color.name()
                case self._together_default_button:
                    self.colors["together"]["Default"] = new_color.name()
                case self._together_d_plusplus_g_minusminus_button:
                    self.colors["together"]["SD++;SG--"] = new_color.name()
                case self._together_d_plusplus_g_minus_button:
                    self.colors["together"]["SD++;SG-"] = new_color.name()
                case self._together_d_plusplus_g_plus_button:
                    self.colors["together"]["SD++;SG+"] = new_color.name()
                case self._together_d_plusplus_g_plusplus_button:
                    self.colors["together"]["SD++;SG++"] = new_color.name()
                case self._together_d_plus_g_minusminus_button:
                    self.colors["together"]["SD+;SG--"] = new_color.name()
                case self._together_d_plus_g_minus_button:
                    self.colors["together"]["SD+;SG-"] = new_color.name()
                case self._together_d_plus_g_plus_button:
                    self.colors["together"]["SD+;SG+"] = new_color.name()
                case self._together_d_plus_g_plusplus_button:
                    self.colors["together"]["SD+;SG++"] = new_color.name()
                case self._together_d_minus_g_minusminus_button:
                    self.colors["together"]["SD-;SG--"] = new_color.name()
                case self._together_d_minus_g_minus_button:
                    self.colors["together"]["SD-;SG-"] = new_color.name()
                case self._together_d_minus_g_plus_button:
                    self.colors["together"]["SD-;SG+"] = new_color.name()
                case self._together_d_minus_g_plusplus_button:
                    self.colors["together"]["SD-;SG++"] = new_color.name()
                case self._together_d_minusminus_g_minusminus_button:
                    self.colors["together"]["SD--;SG--"] = new_color.name()
                case self._together_d_minusminus_g_minus_button:
                    self.colors["together"]["SD--;SG-"] = new_color.name()
                case self._together_d_minusminus_g_plus_button:
                    self.colors["together"]["SD--;SG+"] = new_color.name()
                case self._together_d_minusminus_g_plusplus_button:
                    self.colors["together"]["SD--;SG++"] = new_color.name()
                case _:
                    raise RuntimeError("ERROR")

from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGraphicsTextItem, QGraphicsItem, QWidget, QStyleOptionGraphicsItem, \
    QGraphicsSceneMouseEvent

TEXT_SEPARATOR = "~"
ALLOWED_CHARACTERS = ["+", "-"]
ALLOWED_STRINGS = ["++", "+", "-", "--"]
HIGHLIGHT_STYLE = "color:white;background-color:#1F51FF;"
UNDERLINE_STYLE = "text-decoration: underline;"


class Descriptor(QGraphicsTextItem):
    """
    This class is a variant of QGraphicsTextItem that is used to set the value of a clause. Those values
    should be SD++, SD+, SD-, SD-- and/or SG--, SG-, SG+, SG++
    """

    highlighted: bool = False
    selected_part: int = 0
    editable_text_list: list[str]
    non_editable_text_list: list[str]
    editable_text_changed = pyqtSignal(QGraphicsTextItem, bool)

    def __init__(self, default_text: str, parent: QGraphicsItem, font: QFont = None) -> None:
        """
        Create Descriptor object.
        :param default_text: The default text that will appear in the descriptor.
        :param parent: The QGraphicsItem parent of this Separator. Can't be None
        :param font: The Descriptor's text font.
        """
        super().__init__(parent)
        self.setPos(0, 0)
        self.setFlag(QGraphicsItem.ItemIgnoresParentOpacity)
        self.points = []
        if font is not None:
            self.setFont(font)

        self.setHtml('<p align="justify">' + default_text + '</p>')

        self.setTextInteractionFlags(Qt.TextEditable)

        self.non_editable_text_list = default_text.split(TEXT_SEPARATOR)
        self.editable_text_list = [TEXT_SEPARATOR] * (len(self.non_editable_text_list) - 1)
        self.selected_part = 0
        self.highlighted = False
        self.style = ""

    def set_default_text(self, default_text: str) -> None:
        """
        Set the default text for this descriptor.
        :param default_text: The default text that will appear in the descriptor.
        """
        self.non_editable_text_list = default_text.split(TEXT_SEPARATOR)
        self.editable_text_list = [TEXT_SEPARATOR] * (len(self.non_editable_text_list) - 1)
        self.selected_part = 0
        self.highlighted = False
        self.update_text("", True)

    def set_text(self, non_editable_text_list: list[str], editable_text_list: list[str]):
        self.non_editable_text_list = non_editable_text_list
        self.editable_text_list = editable_text_list
        self.selected_part = 0
        self.highlighted = False
        self.update_text("", True)

    def copy_text(self) -> tuple[list[str], int, bool, str]:
        """
        Copy the relevant information to set the text behaviour. This configuration should be used to set the
        configuration of another descriptor via "paste_text" function.
        """
        return (
            self.editable_text_list,
            self.selected_part,
            self.highlighted,
            self.style
        )

    def paste_text(self, info: tuple[list[str], int, bool, str]) -> None:
        """
        Paste the relevant information to set the text behaviour. This configuration should come from another
        descriptor. To avoid time-consuming logic, the text only changes if the information is not the same as the
        original in this element.

        :param info: The information to set the text behaviour.
        """
        if (self.editable_text_list != info[0] or
                self.selected_part != info[1] or self.highlighted != info[2] or self.style != info[3]):
            self.editable_text_list = info[0].copy()
            self.selected_part = info[1]
            self.highlighted = info[2]
            self.style = info[3]
            self.document().setHtml(self.style_editable_text(self.selected_part, self.style))

    def update_text(self, style: str, text_changed: bool) -> None:
        """
        Update the content of the QTextDocument with the info in self.editable_text_list and
        self.non_editable_text_list. Also update the text position.
        :param style: A string with CSS format that contains the style of the text
        :param text_changed: A boolean that indicates if the text has been modified or only the font
        """
        self.style = style
        self.document().setHtml(self.style_editable_text(self.selected_part, style))
        self.emit_text_changed(text_changed)

    def emit_text_changed(self, text_changed: bool) -> None:
        self.editable_text_changed.emit(self, text_changed)

    def style_editable_text(self, index: int, style: str) -> str:
        """
        Gives style to the n-editable-text-part in the text. The n-editable-text-part styled is given
        by the ind parameter.
        :param index: Index of editable text part that is going to be styled.
        :param style: A string with CSS format that contains the style of the text
        :return: The resulting string
        """
        aux = ""
        for i in range(len(self.editable_text_list)):
            if i == index:
                aux += (self.non_editable_text_list[i] + "<span style='" + style + "'>" + self.editable_text_list[i])
            elif i == index + 1:
                aux += ("</span>" + self.non_editable_text_list[i] + self.editable_text_list[i])
            else:
                aux += (self.non_editable_text_list[i] + self.editable_text_list[i])

        if index == len(self.editable_text_list) - 1:
            aux += ("</span>" + self.non_editable_text_list[-1])
        else:
            aux += self.non_editable_text_list[-1]

        return aux

    def setFont(self, font: QtGui.QFont) -> None:
        """
        Set text with a given font.
        :param font: The font object
        """
        super().setFont(font)
        self.update()

    def focusOutEvent(self, event: QtGui.QFocusEvent) -> None:
        """
        Manages the behaviour of the Descriptor when the user click in an area that is not the Descriptor.
        In this case, the object removes all the custom styles applied to the text.
        :param event: The object that indicates the type of event triggered. In this case is a QFocusEvent
        """
        self.update_text("", False)
        super().focusOutEvent(event)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        """
        Manages the behaviour of the Descriptor when the user release the object. In this case, the object highlight
        part of the text.
        :param event: The object that indicates the type of event triggered. In this case is a QGraphicsSceneMouseEvent
        """
        if event.button() is not Qt.RightButton:
            self.selected_part = 0
            self.update_text(HIGHLIGHT_STYLE, False)
            self.highlighted = True
        super().mousePressEvent(event)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        """
        Handle keyboard press events. In this case, edits the position of the texts and the text
        :param event: The object that indicates the type of event triggered. In this case, has information
                      about the key pressed
        """
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.selected_part += 1
            if self.selected_part < len(self.non_editable_text_list):
                self.update_text(HIGHLIGHT_STYLE, False)
                self.highlighted = True

        elif self.selected_part < len(self.editable_text_list):  # If we have selected a valid editable text part
            if event.key() == Qt.Key_Backspace:  # Remove last char
                if self.highlighted:
                    self.highlighted = False
                    self.editable_text_list[self.selected_part] = ""
                else:
                    self.editable_text_list[self.selected_part] = self.editable_text_list[self.selected_part][:-1]
                if self.editable_text_list[self.selected_part] == "":  # If no chars, add default char
                    self.editable_text_list[self.selected_part] = TEXT_SEPARATOR
                    self.update_text(HIGHLIGHT_STYLE, True)
                else:
                    self.update_text(UNDERLINE_STYLE, True)
            elif Qt.Key_Space <= event.key() <= Qt.Key_ydiaeresis:  # If readable character
                char = chr(event.key())
                if char in ALLOWED_CHARACTERS:  # If valid char
                    if self.highlighted:
                        self.highlighted = False
                        self.editable_text_list[self.selected_part] = char
                        self.update_text(UNDERLINE_STYLE, True)
                    elif self.editable_text_list[self.selected_part] == TEXT_SEPARATOR:
                        self.editable_text_list[self.selected_part] = char
                        self.update_text(UNDERLINE_STYLE, True)
                    elif (self.editable_text_list[self.selected_part] + char) in ALLOWED_STRINGS:
                        self.editable_text_list[self.selected_part] += char
                        self.update_text(UNDERLINE_STYLE, True)

    def paint(self, painter: QtGui.QPainter, option: QStyleOptionGraphicsItem, widget: QWidget) -> None:
        painter.setFont(self.font())
        self.document().drawContents(painter)

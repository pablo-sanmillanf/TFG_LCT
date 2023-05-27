from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGraphicsTextItem, QGraphicsItem, QWidget, QStyleOptionGraphicsItem, \
    QGraphicsSceneMouseEvent

HIGHLIGHT_STYLE = "color:white;background-color:#1F51FF;"
UNDERLINE_STYLE = "text-decoration: underline;"


class Descriptor(QGraphicsTextItem):
    """
    This class is a variant of QGraphicsTextItem that is used to set the value of a clause.
    """

    _highlighted: bool = False
    _selected_part: int = 0
    _editable_text_list: list[str]
    _non_editable_text_list: list[str]
    editable_text_changed = pyqtSignal(QGraphicsTextItem, bool)

    def __init__(self, default_text: str, text_separator: str, allowed_strings: list[str], parent: QGraphicsItem,
                 font: QFont = None) -> None:
        """
        Create Descriptor object.
        :param default_text: The default text that will appear in the descriptor.
        :param text_separator: The part of the text that will be substituted by a valid value.
        :param allowed_strings: A list of string with the valid values.
        :param parent: The QGraphicsItem parent of this Separator. Can't be None
        :param font: The Descriptor's text font.
        """
        super().__init__(parent)
        self._text_separator = text_separator
        self._allowed_strings = allowed_strings
        self._allowed_chars = list(set("".join(self._allowed_strings)))
        self.setPos(0, 0)
        self.setFlag(QGraphicsItem.ItemIgnoresParentOpacity)
        if font is not None:
            self.setFont(font)

        self.setHtml('<p align="justify">' + default_text + '</p>')

        self.setTextInteractionFlags(Qt.TextEditable)

        self._non_editable_text_list = default_text.split(self._text_separator)
        self._editable_text_list = [self._text_separator] * (len(self._non_editable_text_list) - 1)
        self._selected_part = 0
        self._highlighted = False
        self._style = ""

    def get_editable_text_list(self) -> list[str]:
        """
        Obtains a copy of the list with the editable parts of the text.
        :return: The editable parts of the text.
        """
        return self._editable_text_list.copy()

    def set_default_text(self, default_text: str) -> None:
        """
        Set the default text for this descriptor.
        :param default_text: The default text that will appear in the descriptor.
        """
        self._non_editable_text_list = default_text.split(self._text_separator)
        self._editable_text_list = [self._text_separator] * (len(self._non_editable_text_list) - 1)
        self._selected_part = 0
        self._highlighted = False
        self._update_text("", True)

    def set_text(self, non_editable_text_list: list[str], editable_text_list: list[str]) -> None:
        """
        Set the text of the descriptor with the non-editable part of the text and the editable part of the text. The
        two lists will be interleaved to achieve the text to be represented in the descriptor.
        :param non_editable_text_list: A list of strings that represents the part of the descriptor that will remain
                                       immutable.
        :param editable_text_list:A list of string that represents the editable part of the descriptor.
        """
        self._non_editable_text_list = non_editable_text_list
        self._editable_text_list = editable_text_list
        self._selected_part = 0
        self._highlighted = False
        self._update_text("", True)

    def copy_text(self) -> tuple[list[str], list[str], int, bool, str]:
        """
        Copy the relevant information to set the text behaviour. This configuration should be used to set the
        configuration of another descriptor via "paste_text" function.
        :return: A tuple with the relevant information.
        """
        return (
            self._non_editable_text_list,
            self._editable_text_list,
            self._selected_part,
            self._highlighted,
            self._style
        )

    def paste_text(self, info: tuple[list[str], list[str], int, bool, str]) -> None:
        """
        Paste the relevant information to set the text behaviour. This configuration should come from another
        descriptor. To avoid time-consuming logic, the text only changes if the information is not the same as the
        original in this element.

        :param info: The information to set the text behaviour.
        """
        if (self._non_editable_text_list != info[0] or self._editable_text_list != info[1] or
                self._selected_part != info[2] or self._highlighted != info[3] or self._style != info[4]):
            self._non_editable_text_list = info[0]
            self._editable_text_list = info[1].copy()
            self._selected_part = info[2]
            self._highlighted = info[3]
            self._style = info[4]
            self.document().setHtml(self._style_editable_text(self._selected_part, self._style))

    def _update_text(self, style: str, text_changed: bool) -> None:
        """
        Update the content of the QTextDocument with the info in self._editable_text_list and
        self._non_editable_text_list.
        :param style: A string with CSS format that contains the style of the text
        :param text_changed: A boolean that indicates if the text has been modified or only the font
        """
        self._style = style
        self.document().setHtml(self._style_editable_text(self._selected_part, style))
        self.emit_text_changed(text_changed)

    def emit_text_changed(self, text_changed: bool) -> None:
        """
        Emits a signal. Called when there have been a change in the text. If the change is only in the font of the text,
        the parameter text_changed should be False, but if the change is in the text itself, should be True.
        :param text_changed: True if the text have changed, False otherwise.
        """
        self.editable_text_changed.emit(self, text_changed)

    def _style_editable_text(self, index: int, style: str) -> str:
        """
        Gives style to the n-editable-text-part in the text. The n-editable-text-part styled is given
        by the ind parameter.
        :param index: Index of editable text part that is going to be styled.
        :param style: A string with CSS format that contains the style of the text
        :return: The resulting string
        """
        aux = ""
        for i in range(len(self._editable_text_list)):
            if i == index:
                aux += (self._non_editable_text_list[i] + "<span style='" + style + "'>" + self._editable_text_list[i])
            elif i == index + 1:
                aux += ("</span>" + self._non_editable_text_list[i] + self._editable_text_list[i])
            else:
                aux += (self._non_editable_text_list[i] + self._editable_text_list[i])

        if index == len(self._editable_text_list) - 1:
            aux += ("</span>" + self._non_editable_text_list[-1])
        else:
            aux += self._non_editable_text_list[-1]

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
        self._update_text("", False)
        super().focusOutEvent(event)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        """
        Manages the behaviour of the Descriptor when the user release the object. In this case, the object highlight
        the first part of the editable text.
        :param event: The object that indicates the type of event triggered. In this case is a QGraphicsSceneMouseEvent
        """
        if event.button() is not Qt.RightButton:
            self._selected_part = 0
            self._update_text(HIGHLIGHT_STYLE, False)
            self._highlighted = True
        super().mousePressEvent(event)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        """
        Handle keyboard press events. In this case, edits the text. Only allowed characters will be added to the
        Descriptor.
        :param event: The object that indicates the type of event triggered. In this case, has information
                      about the key pressed
        """
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self._selected_part += 1
            if self._selected_part < len(self._non_editable_text_list):
                self._update_text(HIGHLIGHT_STYLE, False)
                self._highlighted = True

        elif self._selected_part < len(self._editable_text_list):  # If we have selected a valid editable text part
            if event.key() == Qt.Key_Backspace:  # Remove last char
                if self._highlighted:
                    self._highlighted = False
                    self._editable_text_list[self._selected_part] = ""
                else:
                    self._editable_text_list[self._selected_part] = self._editable_text_list[self._selected_part][:-1]
                if self._editable_text_list[self._selected_part] == "":  # If no chars, add default char
                    self._editable_text_list[self._selected_part] = self._text_separator
                    self._update_text(HIGHLIGHT_STYLE, True)
                else:
                    self._update_text(UNDERLINE_STYLE, True)
            elif Qt.Key_Space <= event.key() <= Qt.Key_ydiaeresis:  # If readable character
                char = chr(event.key())
                if char in self._allowed_chars:  # If valid char
                    if self._highlighted:
                        self._highlighted = False
                        self._editable_text_list[self._selected_part] = char
                        self._update_text(UNDERLINE_STYLE, True)
                    elif self._editable_text_list[self._selected_part] == self._text_separator:
                        self._editable_text_list[self._selected_part] = char
                        self._update_text(UNDERLINE_STYLE, True)
                    elif (self._editable_text_list[self._selected_part] + char) in self._allowed_strings:
                        self._editable_text_list[self._selected_part] += char
                        self._update_text(UNDERLINE_STYLE, True)

    def paint(self, painter: QtGui.QPainter, option: QStyleOptionGraphicsItem, widget: QWidget) -> None:
        """
        Paints the text of the descriptor using the information stored in the QTextDocument. This method has been
        override to remove extra elements that the QGraphicsText paints by default such as the cursor.
        :param painter: The object to paint the text in the canvas
        :param option: This parameter will be ignored
        :param widget: This parameter will be ignored
        """
        painter.setFont(self.font())
        self.document().drawContents(painter)

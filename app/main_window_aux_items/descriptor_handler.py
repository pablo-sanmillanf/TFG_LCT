import typing

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QPointF, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGraphicsTextItem, QWidget, QStyleOptionGraphicsItem, QGraphicsItem, \
    QGraphicsSceneMouseEvent

from .separator import Separator

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
    editable_text_changed = pyqtSignal(list)

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

    def set_default_text(self, default_text: str) -> None:
        """
        Set the default text for this descriptor.
        :param default_text: The default text that will appear in the descriptor.
        """
        self.setHtml('<p align="justify">' + default_text + '</p>')
        self.non_editable_text_list = default_text.split(TEXT_SEPARATOR)
        self.editable_text_list = [TEXT_SEPARATOR] * (len(self.non_editable_text_list) - 1)
        self.selected_part = 0
        self.highlighted = False
        self.update_text("")

    def get_text_height(self) -> float:
        """
        This function gets the height in pixels of the text item with the given font.
        :return: The height that occupies the text
        """
        aux = QGraphicsTextItem()
        aux.setFont(self.font())

        aux.setHtml('<p align="justify">Test</p>')

        return aux.boundingRect().height()

    def get_separator_offsets_height(self) -> float:
        """
        This function gets the height in pixels of the padding introduced by the QGraphicsTextItem
        element. To do so,the following system of equations must be solved:
            - padding + strip + padding = height_1
            - padding + strip + strip + padding = height_2
        Those values will be used to place the text

        :return: The padding height introduced by QGraphicsTextItem.
        """
        aux = QGraphicsTextItem()
        aux.setFont(self.font())

        aux.setHtml('<p align="justify">Test</p>')
        height_1 = aux.boundingRect().height()

        aux.setHtml('<p align="justify">Test<br>Test</p>')
        height_2 = aux.boundingRect().height()

        return height_1 - height_2 / 2

    def update_text(self, style: str) -> None:
        """
        Update the content of the QTextDocument with the info in self.editable_text_list and
        self.non_editable_text_list. Also update the text position.
        :param style: A string with CSS format that contains the style of the text
        """
        self.document().setHtml(self.style_editable_text(self.selected_part, style))
        self.editable_text_changed.emit(self.editable_text_list)

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
        self.document().setHtml(self.style_editable_text(self.selected_part, ""))
        super().focusOutEvent(event)

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        """
        Manages the behaviour of the Descriptor when the user release the object. In this case, the object highlight
        part of the text.
        :param event: The object that indicates the type of event triggered. In this case is a QGraphicsSceneMouseEvent
        """
        if event.button() is not Qt.RightButton:
            self.selected_part = 0
            self.document().setHtml(self.style_editable_text(self.selected_part, HIGHLIGHT_STYLE))
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
                self.document().setHtml(self.style_editable_text(self.selected_part, HIGHLIGHT_STYLE))
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
                    self.update_text(HIGHLIGHT_STYLE)
                else:
                    self.update_text(UNDERLINE_STYLE)
            elif Qt.Key_Space <= event.key() <= Qt.Key_ydiaeresis:  # If readable character
                char = chr(event.key())
                if char in ALLOWED_CHARACTERS:  # If valid char
                    if self.highlighted:
                        self.highlighted = False
                        self.editable_text_list[self.selected_part] = char
                        self.update_text(UNDERLINE_STYLE)
                    elif self.editable_text_list[self.selected_part] == TEXT_SEPARATOR:
                        self.editable_text_list[self.selected_part] = char
                        self.update_text(UNDERLINE_STYLE)
                    elif (self.editable_text_list[self.selected_part] + char) in ALLOWED_STRINGS:
                        self.editable_text_list[self.selected_part] += char
                        self.update_text(UNDERLINE_STYLE)

    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionGraphicsItem', widget: QWidget) -> None:
        painter.setFont(self.font())
        self.document().drawContents(painter)


class DescriptorHandler:
    """
        This class is a variant of QGraphicsTextItem that is used to set the value of a clause. Those values
        should be SD++, SD+, SD-, SD-- and/or SG--, SG-, SG+, SG++
        """
    descriptors: list[list[Descriptor | float | float | float]]
    points: list[tuple[float | int, tuple[float | int, float | int]]]
    padding_height: float
    editable_text_changed = pyqtSignal(list)

    def __init__(self, y_offset: int | float, default_text: str, text_size: float | int,
                 points: list[tuple[float | int, tuple[float | int, float | int]]], parent: QGraphicsItem,
                 font: QFont = None) -> None:
        """
        Create Descriptor object.
        :param y_offset: Set y offset for all the points calculated.
        :param default_text: The default text that will appear in the descriptor.
        :param text_size: The size of the text as a point size.
        :param parent: The QGraphicsItem parent of this Separator. Can't be None
        :param font: The Descriptor's text font.
        """
        self.parent = parent
        self.points = points
        self.y_offset = y_offset
        self.default_text = default_text

        if font is None:
            self.font = QGraphicsTextItem().font()
        else:
            self.font = font

        self.descriptors = []
        self.padding_height = self.get_separator_offsets_height()

        for i in range(len(points)):
            desc = Descriptor(default_text, parent, font)
            # [Descriptor, Y_Value_Without_Offset, Left_X_Value, Right_X_Value]
            self.descriptors.append([desc, self.points[i][0], self.points[i][1][0], self.points[i][1][-1]])
            self.set_descriptor_pos(i)

        self.separators = []

        self.set_text_size(text_size)

    def add_separator_listeners(self, pos_changed_fn: typing.Any, clicked_on_the_border_fn: typing.Any) -> None:
        pos_changed_fn.connect(self.separator_position_changed)
        clicked_on_the_border_fn.connect(self.separator_clicked_on_the_border)

    def set_descriptor_pos(self, ind):
        rect = self.descriptors[ind][0].boundingRect()
        self.descriptors[ind][0].setPos(
            (self.descriptors[ind][3] + self.descriptors[ind][2] - rect.width()) / 2,
            self.descriptors[ind][1] + self.y_offset + self.padding_height + rect.height()
        )
        if self.descriptors[ind][3] == self.descriptors[ind][2]:
            self.descriptors[ind][0].hide()
        else:
            self.descriptors[ind][0].show()

    def set_default_text(self, default_text: str) -> None:
        """
        Set the default text for this descriptor.
        :param default_text: The default text that will appear in the descriptor.
        """
        for i in range(len(self.descriptors)):
            self.descriptors[i][0].set_default_text(default_text)

            self.set_descriptor_pos(i)

    def get_separator_offsets_height(self) -> float:
        """
        This function gets the height in pixels of the padding introduced by the QGraphicsTextItem
        element. To do so,the following system of equations must be solved:
            - padding + strip + padding = height_1
            - padding + strip + strip + padding = height_2
        Those values will be used to place the text

        :return: The padding height introduced by QGraphicsTextItem.
        """
        aux = QGraphicsTextItem()
        aux.setFont(self.font)

        aux.setHtml('<p align="justify">Test</p>')
        height_1 = aux.boundingRect().height()

        aux.setHtml('<p align="justify">Test<br>Test</p>')
        height_2 = aux.boundingRect().height()

        return height_1 - height_2 / 2

    def set_text_size(self, text_size: float | int) -> None:
        """
        Set the text size.
        :param text_size: The text size as a number.
        """
        font = self.font
        font.setPointSize(int(text_size))

        self.setFont(font)

    def setFont(self, font: QtGui.QFont) -> None:
        """
        Set text with a given font.
        :param font: The font object
        """
        self.font = font
        self.padding_height = self.get_separator_offsets_height()

        for i in range(len(self.descriptors)):
            self.descriptors[i][0].setFont(font)

            self.set_descriptor_pos(i)

    def find_separator(self, separator: Separator) -> int:
        for i in range(len(self.separators)):
            if self.separators[i][0] is separator:
                return i

    def add_separator(self, separator: Separator, point: QPointF):
        if len(self.separators) == 0:
            self.separators.append([separator, self.insert_descriptor(point), point])
        else:
            for i in range(len(self.separators)):
                if (point.y() > self.separators[i][0].pos().y() or
                        (point.y() == self.separators[i][0].pos().y() and
                         point.x() > self.separators[i][0].pos().x())):
                    # [Separator, Last_index_before, Last_position]
                    self.separators.insert(i + 1, [separator, self.insert_descriptor(point), point])

                    # Update "Last_index_before" for the separators after this separator
                    for e in range(i + 2, len(self.separators)):
                        self.separators[e][1] += 1
                    return

            # If the separator is inserted after the first immobile separator
            self.separators.insert(0, [separator, self.insert_descriptor(point), point])

            # Update "Last_index_before" for the separators after this separator
            for e in range(1, len(self.separators)):
                self.separators[e][1] += 1

    def insert_descriptor(self, point: QPointF):

        for i in range(len(self.descriptors)):
            if (point.y() < self.descriptors[i][1] or
                    (point.y() == self.descriptors[i][1] and point.x() < self.descriptors[i][2])):
                self.descriptors.insert(
                    i,
                    [
                        Descriptor(self.default_text, self.parent, self.font),
                        point.y(),
                        point.x(),
                        self.descriptors[i - 1][3]
                    ]
                )
                self.set_descriptor_pos(i)

                self.descriptors[i - 1][3] = point.x()
                self.set_descriptor_pos(i - 1)

                return i - 1

    def update_downwards(self, index, point: QPointF):
        for i in range(index, len(self.descriptors)):
            if point.y() > self.descriptors[i][1]:
                self.descriptors[i][3] = self.descriptors[i + 1][3]
                self.set_descriptor_pos(i)

                self.descriptors[i + 1][1] = self.descriptors[i + 2][1]
                self.descriptors[i + 1][2] = self.descriptors[i + 2][2]
            else:
                self.descriptors[i + 1][2] = point.x()
                self.descriptors[i + 1][1] = self.descriptors[i][1]
                self.set_descriptor_pos(i + 1)

                self.descriptors[i][3] = point.x()
                self.set_descriptor_pos(i)
                return i
        raise RuntimeError("DOWNWARDS FINISH WITHOUT RETURNING")

    def update_upwards(self, index, point: QPointF):
        for i in range(index, -1, -1):
            if point.y() < self.descriptors[i][1]:

                self.descriptors[i + 1][1] = self.descriptors[i][1]
                self.descriptors[i + 1][2] = self.descriptors[i][2]
                self.set_descriptor_pos(i + 1)

                self.descriptors[i][3] = self.descriptors[i - 1][3]
            else:
                self.descriptors[i + 1][1] = self.descriptors[i][1]
                self.descriptors[i + 1][2] = point.x()
                self.set_descriptor_pos(i + 1)

                self.descriptors[i][3] = point.x()
                self.set_descriptor_pos(i)
                return i
        raise RuntimeError("UPWARDS FINISH WITHOUT RETURNING")

    def separator_position_changed(self, moved_separator: QGraphicsItem, point: QPointF) -> None:
        """
        Updates the rectangle positions and length according to the new position of moved_separator. This function
        should be called every time a Separator has moved.
        :param moved_separator: The separator that has moved.
        :param point: The position of the separator.
        """
        sep_index = self.find_separator(moved_separator)

        if sep_index is None:
            self.add_separator(moved_separator, point)
        else:
            if (point.y() < self.separators[sep_index][2].y() or
                    (point.y() == self.separators[sep_index][2].y() and
                     point.x() < self.separators[sep_index][2].x())):  # Separator moved upwards
                self.separators[sep_index][1] = self.update_upwards(self.separators[sep_index][1], point)

            elif (point.y() > self.separators[sep_index][2].y() or
                  (point.y() == self.separators[sep_index][2].y() and
                   point.x() > self.separators[sep_index][2].x())):  # Separator moved downwards
                self.separators[sep_index][1] = self.update_downwards(self.separators[sep_index][1], point)

            self.separators[sep_index][2] = point

    def separator_clicked_on_the_border(self, moved_separator: QGraphicsItem, cursor_point: QPointF,
                                        right_point: QPointF, left_point: QPointF) -> None:
        sep_index = self.find_separator(moved_separator)

        if sep_index is None:
            self.add_separator(moved_separator, right_point)
        else:
            # If the user released the separator in the right border and now the user is clicking in the left border
            # if self.separators[sep_index][2] == right_point and \
            #        (cursor_point - right_point).manhattanLength() > (cursor_point - left_point).manhattanLength():
            # Nothing is done because of the way function "update_downwards" is designed.

            # If the user released the separator in the left border and now the user is clicking in the right border
            if self.separators[sep_index][2] == left_point and \
                    (cursor_point - left_point).manhattanLength() > (cursor_point - right_point).manhattanLength():
                # Auxiliary variable to add clarity
                ind = self.separators[sep_index][1]

                self.descriptors[ind][1] = self.descriptors[ind - 1][1]
                self.descriptors[ind][2] = self.descriptors[ind - 1][3]
                self.descriptors[ind][3] = self.descriptors[ind - 1][3]
                self.set_descriptor_pos(ind)

                self.separators[sep_index][1] -= 1

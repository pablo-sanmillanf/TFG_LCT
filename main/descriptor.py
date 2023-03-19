import typing

import numpy as np
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QRectF, QPointF, QEvent
from PyQt5.QtGui import QPainterPath, QCursor, QTextDocument
from PyQt5.QtWidgets import QGraphicsTextItem, QWidget, QStyleOptionGraphicsItem, QGraphicsItem, QGraphicsRectItem, \
    QGraphicsSceneMouseEvent

from separator import Separator


# Validating text:
# https://stackoverflow.com/questions/17079535/qt-editable-qgraphicstextitem-validating-text-and-emitting-signal-on-change

class Descriptor(QGraphicsTextItem):
    """
    This class is a variant of QGraphicsTextItem that is used to set the value of a clause. Those values
    should be SD++, SD+, SD-, SD-- and/or SG--, SG-, SG+, SG++
    """
    def __init__(self, max_width, text, parent, font=None):
        super().__init__(parent)
        self.setPos(0, 0)

        self.left_separator = None
        self.right_separator = None

        self.points = []

        if font is not None:
            self.setFont(font)

        self.width = self.get_text_width(text)
        self.height = self.get_text_height()
        self.setHtml('<p align="justify">' + text + '</p>')

        self.padding_width = self.get_separator_offsets_width()
        self.padding_height = self.get_separator_offsets_height()[0]

        self.size = [max_width, 500]

        self.setTextInteractionFlags(Qt.TextEditable)

    def get_text_width(self, text):
        """
        This function gets the width in pixels of the given text with the given font.
        :param text: The text to calculate the width.
        :return: The width that occupies the text.
        """
        text_item = QGraphicsTextItem(text)
        text_item.setFont(self.font())

        return text_item.boundingRect().width()

    def get_text_height(self) -> float:
        """
        This function gets the height in pixels of the text item with the given font.
        :return: The height that occupies the text
        """
        aux = QGraphicsTextItem()
        aux.setFont(self.font())

        aux.setHtml('<p align="justify">Test</p>')

        return aux.boundingRect().height()

    def get_separator_offsets_width(self) -> tuple:
        """
        This function gets the width in pixels of the padding introduced by the QGraphicsTextItem
        element. To do this, the following system of equations must be solved:
            - padding + space + padding = len_text1
            - padding + space + space + padding = len_text2
        Those values will be used to place the text

        :return: The padding introduced by QGraphicsTextItem.
        """
        text1 = QGraphicsTextItem(" ")
        text2 = QGraphicsTextItem("  ")
        text1.setFont(self.font())
        text2.setFont(self.font())

        return text1.boundingRect().width() - text2.boundingRect().width() / 2

    def get_separator_offsets_height(self) -> tuple:
        """
        This function gets the height in pixels of the height of the strip used to represent
        the text with the given font. In addition, it also gets the height in pixels of the
        padding introduced by the QGraphicsTextItem element. To do so,the following system of
        equations must be solved:
            - padding + strip + padding = height_1
            - padding + strip + strip + padding = height_2
        Those values will be used to place the text

        :return:
            - padding: The padding height introduced by QGraphicsTextItem.
            - strip: The height that occupies the text
        """
        aux = QGraphicsTextItem()
        aux.setFont(self.font())

        aux.setHtml('<p align="justify">Test</p>')
        height_1 = aux.boundingRect().height()

        aux.setHtml('<p align="justify">Test<br>Test</p>')
        height_2 = aux.boundingRect().height()

        # Resolve the system of equations
        padding = height_1 - height_2 / 2
        strip = height_2 - height_1

        return padding, strip

    def init_separators(self, separators: tuple[Separator, Separator]) -> None:
        """
        Set the separators that the object will follow. When the separators are moved, the number of text
        and the position of its will change.
        :param separators: A tuple with left and right separators
        """
        if not isinstance(separators, (np.ndarray, tuple, list)):
            raise TypeError('separators must be a list')
        if not all(isinstance(x, Separator) for x in separators):
            raise TypeError('All the elements of separators must be of type Separator')
        if self.left_separator is not None:
            self.left_separator.removeSceneEventFilter(self)
        if self.right_separator is not None:
            self.right_separator.removeSceneEventFilter(self)
        self.left_separator = separators[0]
        self.right_separator = separators[1]
        self.left_separator.installSceneEventFilter(self)
        self.right_separator.installSceneEventFilter(self)

        self.set_points(self.left_separator)

    def get_lines_y_values(self) -> list[float]:
        """
        Find the y values of the lines to be filled by this MultilineRoundedRect
        :return: The list with the y values
        """
        lines = []
        for y_value in sorted(set(self.left_separator.get_y_values() + self.right_separator.get_y_values())):
            if self.left_separator.pos().y() <= y_value <= self.right_separator.pos().y():
                lines.append(y_value)
        return lines

    def set_points(self, moved_separator: Separator) -> None:
        """
        Fill the list self.points with the values to be used to paint the rectangles. Each position of the
        list is: (X_position, Y_position, Width).
        This function is called every time a Separator has moved.
        :param moved_separator: The separator that has moved. Can be left_separator or right_separator
        """
        lines = self.get_lines_y_values()
        self.points.clear()
        self.set_bounding_rect(lines)
        if len(lines) == 1:
            self.points.append(
                QPointF(
                    (self.right_separator.pos().x() + self.left_separator.pos().x() - self.width) / 2,  # X Value
                    self.left_separator.pos().y(),  # Y Value
                )
            )
        elif len(lines) > 1:
            # Set first line rounded rectangle
            first_line_x_values = moved_separator.get_x_values(lines[0])

            # It will always be true except if left_separator is in the last x position of
            # a line and the right_separator is moving
            if first_line_x_values is not None:
                self.points.append(
                    QPointF(
                        (self.left_separator.pos().x() + first_line_x_values[-1] - self.width) / 2,  # X Value
                        lines[0],  # Y Value
                    )
                )

            # Set the rest of line rounded rectangles except the last one
            for i in range(1, len(lines) - 1):
                x_values = moved_separator.get_x_values(lines[i])
                self.points.append(
                    QPointF(
                        (x_values[0] + x_values[-1] - self.width) / 2,  # X Value
                        lines[i],  # Y Value
                    )
                )

            # Set the last line rounded rectangle
            last_line_x_values = moved_separator.get_x_values(lines[-1])

            # It will always be true except if right_separator is in the first x position of
            # a line and the left_separator is moving
            if last_line_x_values is not None:
                self.points.append(
                    QPointF(
                        (last_line_x_values[0] + self.right_separator.pos().x() - self.width) / 2,  # X Value
                        self.right_separator.pos().y(),  # Y Value
                    )
                )
        else:
            raise TypeError('Separators swapped')

    def set_bounding_rect(self, lines):
        """
        Set the bounding rect size and position according to the y vales given.
        :param lines: The list with the y values
        """
        self.setPos(self.pos().x(), lines[0] + self.height)
        self.size[1] = lines[-1] + self.height - lines[0]

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        super().keyPressEvent(event)
        self.width = self.get_text_width(self.document().toPlainText())
        self.set_points(self.left_separator)

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, self.size[0], self.size[1])

    def shape(self) -> QPainterPath:
        path = QPainterPath()
        self.width = self.get_text_width(self.document().toPlainText())
        offset = -self.pos() + QPointF(0, self.height - self.padding_height)
        for point in self.points:
            path.addRect(QRectF(point + offset, point + offset + QPointF(self.width, self.height)))
        return path

    def paint(self,
              painter: QtGui.QPainter,
              option: "QStyleOptionGraphicsItem",
              widget: typing.Optional[QWidget] = ...) -> None:
        """
        Paints the text descriptors using the information stored in self.points.
        :param painter: The object to paint the text in the canvas
        :param option: This parameter will be ignored
        :param widget: This parameter will be ignored
        """
        painter.setFont(self.font())
        previous_point = self.pos() + QPointF(0, -self.height + self.padding_height)
        for i in range(len(self.points)):
            painter.translate(self.points[i] - previous_point)
            self.document().drawContents(painter)
            previous_point = self.points[i]

    def sceneEventFilter(self, watched: QGraphicsItem, event: QEvent) -> bool:
        """
        Filters events for the item watched. event is the filtered event.

        In this case, this function only watch Separator items, and it is used to update the number of
        text-boxes displayed and its positions.

        :param watched: Item from which the event has occurred
        :param event: The object that indicates the type of event triggered
        :return: False, to allow the event to be treated by other Items
        """
        if isinstance(event, QGraphicsSceneMouseEvent) or \
                (isinstance(event, QEvent) and event.type() == QEvent.UngrabMouse):
            if self.right_separator is watched or self.left_separator is watched:
                self.set_points(watched)
        return False

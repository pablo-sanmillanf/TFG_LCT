from typing import Any

import numpy as np
from PyQt5 import QtGui
from PyQt5.QtCore import QPointF

from PyQt5.QtWidgets import (
    QGraphicsTextItem, QGraphicsItem,
)


class CustomText(QGraphicsTextItem):
    """
    This class represents a multiline text with an interline spacing introduced in the constructor.
    To insert line breaks, the characters "<br>" surrounded by spaces must be entered in the text.
    If these conditions are not met, a malfunction results.
    """
    point_list: list[Any]

    def __init__(self, text, width, line_height, parent):
        super().__init__(parent)
        self.setTextWidth(width - 10)
        self.setFlag(QGraphicsItem.ItemIgnoresParentOpacity)
        self.setPos(5, 5)
        self.setZValue(1)
        self.line_height = line_height
        self.point_list = []
        self.text = text
        self.set_text(text)

    def set_text(self, text) -> None:
        """
        Set the text of the element justified and with the element's line height.
        :param text: The text
        """
        self.text = text
        self.setHtml('<p align="justify" style="line-height: ' + str(self.line_height) + '%">' + text + '</p>')

        self.set_separator_points(text.split(" "))

    def set_width(self, width: float | int) -> None:
        """
        Set the text width for the item and recalculates the separator points
        :param width: Maximum width in pixels
        """
        self.setTextWidth(width - 10)
        self.set_separator_points(self.text.split(" "))

    def set_separator_points(self, text_list: list) -> None:
        """
        This function calculates the points of separation between the different words of
        a given text.
        :param text_list: List of the words of the text
        """
        lines = self.get_lines(text_list)
        padding, strip, line_spacing = self.set_separator_offsets_height()
        self.point_list.clear()

        for i in range(len(lines)):
            self.point_list.append(
                (
                    padding + (strip + line_spacing) * i + self.pos().y(),
                    self.get_line_separator_points(lines[i][0], lines[i][1])
                )
            )

    def get_line_separator_points(self, text: str, last_line: bool) -> np.ndarray:
        """
        This function calculates the word separations for a given line. Since the text is
        justified, the line_height of each space character will vary according to how much the
        words on that line occupy to fit the total length.

        :param text: The text of the given line
        :param last_line: A boolean that indicates if it is the last line. This will be
                          useful to calculate the space character length
        :return: A list with the x values
        """
        # Check parameters
        if not isinstance(last_line, bool):
            raise TypeError('last_line must be a boolean')
        if not isinstance(text, str):
            raise TypeError('text must be a string')

        text_list = text.split(" ")
        points = np.empty(len(text_list) + 1, dtype=object)

        # Create an auxiliary QGraphicsTextItem to calculate the points
        aux_text = QGraphicsTextItem()
        aux_text.setFont(self.font())

        # Obtain the offsets to correctly place the separators
        half_space, padding = self.set_separator_offsets_width()

        # Adjust offsets to the justify line
        if not last_line:
            aux_text.setPlainText(text)

            # We obtain the remaining pixels that will be distributed among all the spaces to
            # justify text, and we divide it by the number of spaces to know how much is left for
            # each one
            space_adjust = (self.textWidth() - aux_text.boundingRect().width()) / (len(text_list) - 1)
        else:
            space_adjust = 0

        # Set
        points[0] = (padding / 2 + self.pos().x(), text_list[0])
        for i in range(len(text_list) - 1):
            aux_text.setPlainText(" ".join(text_list[:i + 1]))

            # Subtract right padding, add half a space and the space adjusts
            points[i + 1] = (
                aux_text.boundingRect().width() - padding +
                half_space + space_adjust / 2 + space_adjust * i + self.pos().x(),
                text_list[i + 1]
            )

        # Set last element
        if not last_line:
            points[-1] = (self.textWidth() - padding / 2 + self.pos().x(), "")
        else:
            aux_text.setPlainText(text)
            points[-1] = (
                aux_text.boundingRect().width() - padding +
                half_space + space_adjust / 2 + space_adjust * (len(text_list) - 1) + self.pos().x(), ""
            )
        return points

    def get_lines(self, text_list: list) -> list:
        """
        Transforms the given list of words into a list of lines, according to the maximum line_height that
        can be occupied by a line. Also gives information abot if a line is the last of its paragraph
        :param text_list: List of the words of the text
        :return: A list of tuples in which each tuple contains a line of text and a boolean indicating
        whether this line is the last line of its paragraph.
        """
        # Create an auxiliary QGraphicsTextItem to calculate the points
        aux_text = QGraphicsTextItem()
        aux_text.setFont(self.font())

        result = []
        init = 0
        for i in range(len(text_list)):
            if text_list[i] == "<br>":
                result.append((" ".join(text_list[init:i]) + "\n", True))
                init = i + 1
            else:
                aux_text.setPlainText(" ".join(text_list[init:i + 1]))
                if aux_text.boundingRect().width() > self.textWidth():
                    result.append((" ".join(text_list[init:i]), False))
                    init = i
        result.append((" ".join(text_list[init:]), True))

        return result

    def set_separator_offsets_width(self) -> tuple:
        """
        This function gets the width in pixels of what would occupy half of what the space
        character occupies with the given font. In addition, it also gets the width in
        pixels of the padding introduced by the QGraphicsTextItem element. To do this, the
        following system of equations must be solved:
            - padding + space + padding = len_text1
            - padding + space + space + padding = len_text2
        Those values will be used to place the text separators

        :return:
            - half_space: Half of what the character space occupies with the given font.
            - padding: The padding introduced by QGraphicsTextItem.
        """
        text1 = QGraphicsTextItem(" ")
        text2 = QGraphicsTextItem("  ")
        text1.setFont(self.font())
        text2.setFont(self.font())

        # Resolve the system of equations
        space = text2.boundingRect().width() - text1.boundingRect().width()
        padding = text1.boundingRect().width() - text2.boundingRect().width() / 2

        return space / 2, padding

    def set_separator_offsets_height(self) -> tuple:
        """
        This function gets the height in pixels of the height of the strip used to represent
        the text with the given font. In addition, it also gets the height in pixels of the
        padding introduced by the QGraphicsTextItem element and of the line spacing. To do so,
        the following system of equations must be solved:
            - padding + strip + padding = height_1
            - padding + strip + line_spacing + padding = height_2
            - padding + strip + line_spacing + strip + line_spacing + padding = height_3
        Those values will be used to place the text separators

        :return:
            - padding: The padding height introduced by QGraphicsTextItem.
            - strip: The height that occupies the text
            - line_spacing: The padding height between line texts
        """
        aux = QGraphicsTextItem()
        aux.setFont(self.font())

        aux.setHtml('<p align="justify">Test</p>')
        height_1 = aux.boundingRect().height()

        aux.setHtml('<p align="justify" style="line-height:' + str(self.line_height) + '%">Test</p>')
        height_2 = aux.boundingRect().height()

        aux.setHtml('<p align="justify" style="line-height:' + str(self.line_height) + '%">Test<br>Test</p>')
        height_3 = aux.boundingRect().height()

        # Resolve the system of equations
        padding = height_2 - (height_3 / 2)
        strip = height_1 - (2 * height_2) + height_3
        line_spacing = height_2 - height_1

        return padding, strip, line_spacing

    def get_points(self) -> list[tuple[float, list[float]]]:
        """
        Return the list of points with this structure:
        [(y_0, [x_0, x_1, ...]), (y_1, [x_0, x_1, ...]), ...]
        :return: The list with the points
        """
        return [(i[0], [e[0] for e in i[1]]) for i in self.point_list]

    def get_points_as_QPointF(self) -> list[QPointF]:
        """
        Returns the list of points as QPointF.
        :return: The list with the points
        """
        points = []
        for line in self.text.point_list:
            for x_value in line[1]:
                points.append(QPointF(x_value[0], line[0]))
        return points

    def setFont(self, font: QtGui.QFont) -> None:
        """
        Set text with a given font.
        :param font: The font object
        """
        super().setFont(font)
        self.set_text(self.text)

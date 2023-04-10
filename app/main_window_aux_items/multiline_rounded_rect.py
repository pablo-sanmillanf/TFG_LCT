import typing

import numpy as np
from PyQt5.QtGui import QColor

from .separator import Separator

from PyQt5.QtCore import QRectF, QPointF
from PyQt5.QtWidgets import (
    QGraphicsRectItem,
    QWidget,
    QStyleOptionGraphicsItem,
    QGraphicsItem,
)
from PyQt5 import QtGui


class MultilineRoundedRect(QGraphicsRectItem):
    """
    This class represents a multiple QGraphicsRectItem with rounded corners. It adjusts his line_height and
    the number of QGraphicsRectItem to fill the gap between the associated Separators.
    Assuming the "|" are the separators and the "=" are the rectangles, this is more or less what it will look like:
    |=====================================================================
    ======================================================================
    ====================================|
    """
    size: list[float | int]
    right_separator: Separator = None
    left_separator: Separator = None
    points: list[tuple[float, float, float]]
    colors: dict[str, str]

    def __init__(self, max_width: float | int, height: float | int, radius: float | int, offset: float | int,
                 colors: dict[str, str], parent: QGraphicsItem) -> None:
        """
        Create MultilineRoundedRect object.
        :param max_width: The maximum width of this element. Is determined by the max text width.
        :param height: The height of the rectangles
        :param radius: The radius of the rounded corners
        :param offset: The space between the border of a separator and
        :param parent: The QGraphicsItem parent of this Separator. Can't be None
        """
        super().__init__(0, 0, 1, height, parent)
        self.color_index = 0
        self.radius = radius
        self.offset = offset
        self.points = []

        self.size = [max_width, height]

        self.setFlag(QGraphicsItem.ItemIgnoresParentOpacity)
        self.colors = colors
        self.editable_text_changed_slot([])

    def init_separators(self, separators: tuple[Separator, Separator]) -> None:
        """
        Set the separators that the object will follow. When the separators are moved, the number of rects
        and the width of the rects will change.
        :param separators: A tuple with left and right separators
        """
        if not isinstance(separators, (np.ndarray, tuple, list)):
            raise TypeError('separators must be a list')
        if not all(isinstance(x, Separator) for x in separators):
            raise TypeError('All the elements of separators must be of type Separator')
        if self.left_separator is not None:
            self.left_separator.emitter.pos_changed.connect(self.separator_position_changed)
        if self.right_separator is not None:
            self.right_separator.emitter.pos_changed.connect(self.separator_position_changed)
        self.left_separator = separators[0]
        self.right_separator = separators[1]
        self.left_separator.emitter.pos_changed.connect(self.separator_position_changed)
        self.right_separator.emitter.pos_changed.connect(self.separator_position_changed)

        self.update_points()

    def set_max_width(self, width: float | int) -> None:
        """
        Set the maximum width for the rounded rects.
        :param width: Maximum width in pixels
        """
        self.prepareGeometryChange()  # Has to be called before bounding rect updating
        self.size[0] = width

    def set_points(self, moved_separator: Separator,
                   left_separator_pos: QPointF, right_separator_pos: QPointF) -> None:
        """
        Fill the list self.points with the values to be used to paint the rectangles. Each position of the
        list is: (X_position, Y_position, Width).
        This function is called every time a Separator has moved.
        :param moved_separator: The separator that has moved. Can be left_separator or right_separator
        :param left_separator_pos: Position of the left separator.
        :param right_separator_pos: Position of the right separator.
        """
        lines = []
        for y_value in sorted(set(self.left_separator.get_y_values() + self.right_separator.get_y_values())):
            if left_separator_pos.y() <= y_value <= right_separator_pos.y():
                lines.append(y_value)

        if len(lines) >= 1:
            self.set_bounding_rect(lines)
            self.points.clear()
            if len(lines) == 1:
                self.points.append(
                    (
                        left_separator_pos.x(),  # X Value
                        left_separator_pos.y(),  # Y Value
                        right_separator_pos.x() - left_separator_pos.x()  # Width
                    )
                )
            elif len(lines) > 1:
                # Set first line rounded rectangle
                first_line_x_values = moved_separator.get_x_values(lines[0])
                self.points.append(
                    (
                        left_separator_pos.x(),  # X Value
                        lines[0],  # Y Value
                        first_line_x_values[-1] - left_separator_pos.x()  # Width
                    )
                )

                # Set the rest of line rounded rectangles except the last one
                for i in range(1, len(lines) - 1):
                    x_values = moved_separator.get_x_values(lines[i])
                    self.points.append(
                        (
                            x_values[0],  # X Value
                            lines[i],  # Y Value
                            x_values[-1] - x_values[0]  # Width
                        )
                    )

                # Set the last line rounded rectangle
                last_line_x_values = moved_separator.get_x_values(lines[-1])
                self.points.append(
                    (
                        last_line_x_values[0],  # X Value
                        right_separator_pos.y(),  # Y Value
                        right_separator_pos.x() - last_line_x_values[0]  # Width
                    )
                )

    def update_points(self) -> None:
        """
        Updates the points to place the rectangles when both separators have been moved at the same time, e.g. when
        resizing the window.
        """
        self.set_points(
            self.left_separator,
            self.left_separator.complete_pos(True),
            self.right_separator.complete_pos(False)
        )

    def set_colors(self, colors: dict[str, str]) -> None:
        """
        Set the colors that will be used by the rounded rect depending on the value of the associated descriptor. The
        length of this dict should be the same as the possible combinations of the descriptor text plus one (the default
        one). Also, the colors list should be of any HTML valid color.
        :param colors: Dict of all available colors and the possibilities for the descriptor
        """
        self.colors = colors
        self.setBrush(QColor(list(self.colors.values())[self.color_index]))
        self.update()

    def set_bounding_rect(self, lines):
        """
        Set the bounding rect line_height and position according to the y vales given.
        :param lines: The list with the y values
        """
        self.setPos(self.pos().x(), lines[0])
        self.prepareGeometryChange()  # Has to be called before bounding rect updating
        self.size[1] = lines[-1] + self.rect().height() - lines[0]

    def boundingRect(self) -> QRectF:
        """
        Returns the bounding rect that occupies the element.
        :return: The bounding rect as a QRectF
        """
        return QRectF(0, 0, self.size[0], self.size[1])

    def paint(self,
              painter: QtGui.QPainter,
              option: "QStyleOptionGraphicsItem",
              widget: typing.Optional[QWidget] = ...) -> None:
        """
        Paints the rectangles using the information stored in self.points and with a given radius.
        :param painter: The object to paint the rectangles in the canvas
        :param option: This parameter will be ignored
        :param widget: This parameter will be ignored
        """
        for point in self.points:
            painter.setBrush(self.brush())
            painter.drawRoundedRect(
                QRectF(
                    self.offset + point[0],  # X Value with certain offset
                    point[1] - self.pos().y(),  # Y Value
                    max(point[2] - 2 * self.offset, 0),  # Width minus left and right offset
                    self.rect().height()  # Height
                ),
                self.radius, self.radius
            )

    def separator_position_changed(self, moved_separator: QGraphicsItem,
                                   left_point: QPointF, right_point: QPointF) -> None:
        """
        Updates the rectangle positions and length according to the new position of moved_separator. If the
        moved_separator is on the border, left_point and right_point represents the left and right positions. If not,
        both points are equal. This function should be called every time a Separator has moved.
        :param moved_separator: The separator that has moved. Can be left_separator or right_separator
        :param left_point: The left position if the separator is in the border.
        :param right_point: The right position if the separator is in the border.
        """
        if moved_separator is self.left_separator:
            self.set_points(moved_separator, left_point, self.right_separator.complete_pos(False))
        elif moved_separator is self.right_separator:
            self.set_points(moved_separator, self.left_separator.complete_pos(True), right_point)

    def editable_text_changed_slot(self, editable_text_list: list[str]) -> None:
        """
        Change the background color of the rect depending on the text values of editable_text_list.
        :param editable_text_list: A list with the editable descriptor text parts.
        """
        index = 0
        editable_text_string = ""
        for i in range(len(editable_text_list)):
            editable_text_string += (str(i) + editable_text_list[i])
        try:
            index = list(self.colors.keys()).index(editable_text_string)
        except ValueError:
            pass
        self.color_index = index
        self.setBrush(QColor(list(self.colors.values())[index]))
        self.update()

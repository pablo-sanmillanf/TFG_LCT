import typing

import numpy as np
from separator import Separator

from PyQt5.QtCore import QEvent, QRectF
from PyQt5.QtWidgets import (
    QGraphicsRectItem,
    QGraphicsSceneMouseEvent,
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
    right_separator: Separator
    left_separator: Separator
    points: list[tuple[float, float, float]]

    def __init__(self, max_width: float | int, height: float | int,
                 radius: float | int, offset: float | int, parent: QGraphicsItem) -> None:
        """
        Create MultilineRoundedRect object.
        :param max_width: The maximum width of this element. Is determined by the max text width.
        :param height: The height of the rectangles
        :param radius: The radius of the rounded corners
        :param offset: The space between the border of a separator and
        :param parent: The QGraphicsItem parent of this Separator. Can't be None
        """
        super().__init__(0, 0, 1, height, parent)
        self.radius = radius
        self.offset = offset
        self.points = []

        self.left_separator = None
        self.right_separator = None

        self.size = [max_width, height]

        self.setFlag(QGraphicsItem.ItemIgnoresParentOpacity)

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
            if self.left_separator.complete_pos(True).y() <= y_value <= self.right_separator.complete_pos(False).y():
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
        if len(lines) >= 1:
            self.set_bounding_rect(lines)
            self.points.clear()
            if len(lines) == 1:
                self.points.append(
                    (
                        self.left_separator.complete_pos(True).x(),  # X Value
                        self.left_separator.complete_pos(True).y(),  # Y Value
                        self.right_separator.complete_pos(False).x() -
                        self.left_separator.complete_pos(True).x()  # Width
                    )
                )
            elif len(lines) > 1:
                # Set first line rounded rectangle
                first_line_x_values = moved_separator.get_x_values(lines[0])

                # It will always be true except if left_separator is in the last x position of
                # a line and the right_separator is moving
                if first_line_x_values is not None:
                    self.points.append(
                        (
                            self.left_separator.complete_pos(True).x(),  # X Value
                            lines[0],  # Y Value
                            first_line_x_values[-1] - self.left_separator.complete_pos(True).x()  # Width
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

                # It will always be true except if right_separator is in the first x position of
                # a line and the left_separator is moving
                if last_line_x_values is not None:
                    self.points.append(
                        (
                            last_line_x_values[0],  # X Value
                            self.right_separator.complete_pos(False).y(),  # Y Value
                            self.right_separator.complete_pos(False).x() - last_line_x_values[0]  # Width
                        )
                    )

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
                    self.offset + point[0],             # X Value with certain offset
                    point[1] - self.pos().y(),          # Y Value
                    max(point[2] - 2*self.offset, 0),   # Width minus left and right offset
                    self.rect().height()                # Height
                ),
                self.radius, self.radius
            )

    def sceneEventFilter(self, watched: QGraphicsItem, event: QEvent) -> bool:
        """
        Filters events for the item watched. event is the filtered event.

        In this case, this function only watch Separator items, and it is used to update the number of rects
        and the width of the rects.

        :param watched: Item from which the event has occurred
        :param event: The object that indicates the type of event triggered
        :return: False, to allow the event to be treated by other Items
        """
        if isinstance(event, QGraphicsSceneMouseEvent) or \
                (isinstance(event, QEvent) and event.type() == QEvent.UngrabMouse):
            if self.right_separator is watched or self.left_separator is watched:
                self.set_points(watched)
                self.scene().views()[0].viewport().repaint()
        return False

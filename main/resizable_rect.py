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
    This class has the same behavior as QGraphicsRectItem except that
    it paints the rectangle with rounded corners, with a rounding radius,
    passed as a parameter in the constructor.
    """
    right_separator: Separator
    left_separator: Separator
    points: list[tuple[float, float, float]]

    def __init__(self, height, radius, offset, parent):
        super().__init__(0, 0, 1, height, parent)
        self.radius = radius
        self.offset = offset
        self.points = []

        self.left_separator = None
        self.right_separator = None

        self.setFlag(QGraphicsItem.ItemIgnoresParentOpacity)

    def init_separators(self, separators: tuple[Separator, Separator]):
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

        self.set_points()

    def get_lines_y_values(self):
        lines = []
        for y_value in self.left_separator.get_y_values():
            if self.left_separator.pos().y() <= y_value <= self.right_separator.pos().y():
                lines.append(y_value)
        return lines

    def set_points(self):
        lines = self.get_lines_y_values()
        self.points.clear()
        if len(lines) == 1:
            self.points.append(
                (
                    self.left_separator.pos().x(),  # X Value
                    self.left_separator.pos().y(),  # Y Value
                    self.right_separator.pos().x() - self.left_separator.pos().x()  # Width
                )
            )
        elif len(lines) > 1:
            # Set first line rounded rectangle
            self.points.append(
                (
                    self.left_separator.pos().x(),  # X Value
                    lines[0],  # Y Value
                    self.left_separator.get_x_values(lines[0])[-1] - self.left_separator.pos().x()  # Width
                )
            )

            # Set the rest of line rounded rectangles except the last one
            for i in range(1, len(lines) - 1):
                x_values = self.left_separator.get_x_values(lines[i])
                self.points.append(
                    (
                        x_values[0],  # X Value
                        lines[i],  # Y Value
                        x_values[-1] - x_values[0]  # Width
                    )
                )

            # Set the last line rounded rectangle
            left_x_border = self.left_separator.get_x_values(lines[-1])[0]
            self.points.append(
                (
                    left_x_border,  # X Value
                    self.right_separator.pos().y(),  # Y Value
                    self.right_separator.pos().x() - left_x_border  # Width
                )
            )
        else:
            raise TypeError('Separators swapped')

    def paint(self,
              painter: QtGui.QPainter,
              option: "QStyleOptionGraphicsItem",
              widget: typing.Optional[QWidget] = ...) -> None:
        for point in self.points:
            painter.drawRoundedRect(
                QRectF(
                    self.offset + point[0],     # X Value with certain offset
                    point[1],                   # Y Value
                    point[2] - 2*self.offset,   # Width minus left and right offset
                    self.rect().height()        # Height
                ),
                self.radius, self.radius
            )

    def sceneEventFilter(self, watched, event):
        if isinstance(event, QGraphicsSceneMouseEvent) or \
                (isinstance(event, QEvent) and event.type() == QEvent.UngrabMouse):
            if self.right_separator is watched or self.left_separator is watched:
                self.set_points()
                self.scene().views()[0].viewport().repaint()
        return False


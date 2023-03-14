import typing

import numpy as np
from separator import Separator

from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import (
    QGraphicsRectItem,
    QGraphicsSceneMouseEvent,
    QWidget,
    QStyleOptionGraphicsItem,
)
from PyQt5 import QtGui


def find_nearest_point(candidate_points, point_reference):
    min_dist = 50000
    final_point = None
    for point in candidate_points:
        distance = np.abs(point_reference.x() - point.x())
        if min_dist > distance:
            min_dist = distance
            final_point = point
    return final_point


class RoundedRect(QGraphicsRectItem):
    """
    This class has the same behavior as QGraphicsRectItem except that
    it paints the rectangle with rounded corners, with a rounding radius,
    passed as a parameter in the constructor.
    """
    def __init__(self, x, y, width, height, radius, *args, **kwargs):
        super().__init__(x, y, width, height, *args, **kwargs)
        self.radius = radius

    def paint(self,
              painter: QtGui.QPainter,
              option: 'QStyleOptionGraphicsItem',
              widget: typing.Optional[QWidget] = ...) -> None:
        painter.drawRoundedRect(self.rect(), self.radius, self.radius)


class ResizableRect(RoundedRect):

    def __init__(self, x, y, width, height, radius, *args, **kwargs):
        super().__init__(0, 0, width, height, radius, *args, **kwargs)

        self.setPos(x, y)

        self.left_separator = None
        self.right_separator = None

    def init_separators(self, separators: tuple[(Separator, float), (Separator, float)]):
        if not isinstance(separators, (np.ndarray, tuple, list)):
            raise TypeError('separators must be a list')

        self.left_separator = separators[0]
        self.right_separator = separators[1]

        if isinstance(self.left_separator, Separator):
            self.left_separator.installSceneEventFilter(self)
        elif not isinstance(self.left_separator, (float, int)):
            raise TypeError('The first element of separators must be of type InLineSeparator or a number')

        if isinstance(self.right_separator, Separator):
            self.right_separator.installSceneEventFilter(self)
        elif not isinstance(self.right_separator, (float, int)):
            raise TypeError('The second element of separators must be of type InLineSeparator or a number')

        self.set_size_and_pos()

    def sceneEventFilter(self, watched, event):
        if isinstance(event, QGraphicsSceneMouseEvent) or \
                (isinstance(event, QEvent) and event.type() == QEvent.UngrabMouse):
            if self.right_separator is watched or self.left_separator is watched:
                self.set_size_and_pos()
        return False

    def set_size_and_pos(self):
        if isinstance(self.left_separator, Separator) and isinstance(self.right_separator, Separator):
            self.setRect(0, 0, self.right_separator.pos().x() - self.left_separator.pos().x(), self.rect().height())
            self.setPos(self.left_separator.pos().x(), self.left_separator.pos().y())

        elif isinstance(self.left_separator, Separator):
            self.setRect(0, 0, self.right_separator - self.left_separator.pos().x(), self.rect().height())
            self.setPos(self.left_separator.pos().x(), self.left_separator.pos().y())

        elif isinstance(self.right_separator, Separator):
            self.setRect(0, 0, self.right_separator.pos().x() - self.left_separator, self.rect().height())
            self.setPos(self.left_separator, self.right_separator.pos().y())

        else:
            self.setRect(0, 0, self.right_separator - self.left_separator, self.rect().height())
            self.setPos(self.left_separator, self.pos().y())


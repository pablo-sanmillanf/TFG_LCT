import typing

import numpy as np
from separator import Separator

from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import (
    QGraphicsRectItem,
    QGraphicsSceneMouseEvent,
    QWidget,
    QStyleOptionGraphicsItem,
    QGraphicsItem,
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
    def __init__(self, x, y, width, height, radius, parent):
        super().__init__(x, y, width, height, parent)
        self.radius = radius

        self.setFlag(QGraphicsItem.ItemIgnoresParentOpacity)

    def paint(self,
              painter: QtGui.QPainter,
              option: 'QStyleOptionGraphicsItem',
              widget: typing.Optional[QWidget] = ...) -> None:
        painter.drawRoundedRect(self.rect(), self.radius, self.radius)

    def __del__(self):
        print("Rounded deleted")


class InLineResizableRect(RoundedRect):

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
            if self.right_separator.main_separator is watched or self.left_separator.main_separator is watched:
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


class ResizableRect(RoundedRect):

    right_separator: Separator
    left_separator: Separator

    def __init__(self, height, radius, parent):
        super().__init__(0, 0, 1, height, radius, parent)

        self.rounded_rects = []
        self.rounded_rects.append(RoundedRect(0, 0, 1, height, radius, self))

    def init_separators(self, separators: tuple[(Separator, float), (Separator, float)]):
        if not isinstance(separators, (np.ndarray, tuple, list)):
            raise TypeError('separators must be a list')
        if not all(isinstance(x, Separator) for x in separators):
            raise TypeError('All the elements of separators must be of type Separator')
        self.left_separator = separators[0]
        self.right_separator = separators[1]
        self.left_separator.installSceneEventFilter(self)
        self.right_separator.installSceneEventFilter(self)

        self.set_size_and_pos()

    def get_lines_y_values(self):
        return list(set(self.left_separator.get_y_values()).intersection(self.right_separator.get_y_values()))

    def sceneEventFilter(self, watched, event):
        if isinstance(event, QGraphicsSceneMouseEvent) or \
                (isinstance(event, QEvent) and event.type() == QEvent.UngrabMouse):
            if self.right_separator.main_separator is watched or self.left_separator.main_separator is watched:
                self.resize_rects_number()
                self.set_size_and_pos()
        return False

    def resize_rects_number(self):

        # Difference between the number of requested and existing inline rounded rectangles
        # If positive, rectangles must be created. If negative rectangles must be removed.
        diff = len(self.get_lines_y_values()) - len(self.rounded_rects)

        if diff == 0:       # Do nothing
            pass
        elif diff > 0:      # Create rectangles
            for i in range(diff):
                self.rounded_rects.append(RoundedRect(0, 0, 1, self.rect().height(), self.radius, self))
        else:               # Delete rectangles
            for i in range(-diff):
                aux_rect = self.rounded_rects.pop(-1)
                self.scene().removeItem(aux_rect)

    def set_size_and_pos(self):
        lines = self.get_lines_y_values()
        if len(lines) == 0:
            self.rounded_rects[0].setRect(
                0,
                0,
                self.right_separator.pos().x() - self.left_separator.pos().x(),
                self.rect().height()
            )
            self.rounded_rects[0].setPos(self.left_separator.pos().x(), self.left_separator.pos().y())
        elif len(lines) > 0:

            # Set first line rounded rectangle
            self.rounded_rects[0].setRect(
                0,
                0,
                self.left_separator.get_x_values(lines[0])[-1] - self.left_separator.pos().x(),
                self.rect().height()
            )
            self.rounded_rects[0].setPos(self.left_separator.pos().x(), lines[0])

            # Set the rest of line rounded rectangles except the last one
            for i in range(1, len(lines) - 1):
                x_values = self.left_separator.get_x_values(lines[i])
                self.rounded_rects[i].setRect(0, 0, x_values[-1] - x_values[0], self.rect().height())
                self.rounded_rects[i].setPos(x_values[0], lines[i])

            # Set the last line rounded rectangle
            left_x_border = self.left_separator.get_x_values(lines[0])[-1]
            self.rounded_rects[-1].setRect(
                0,
                0, self.right_separator.pos().x() - left_x_border,
                self.rect().height()
            )
            self.rounded_rects[-1].setPos(left_x_border, self.right_separator.pos().y())

        else:
            raise TypeError('Separators swapped')



import typing

import numpy as np
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsItem
from PyQt5.QtCore import QEvent


def find_nearest_point(candidate_points: list, point_reference: float) -> tuple[float, int]:
    """
    Find the nearest float to point_reference from the list candidate_points.
    :param candidate_points: A list of floats with the possible values
    :param point_reference: The float to compare with
    :return: The nearest float in the list and its index
    """

    nearest_point_index = 0
    nearest_point = candidate_points[0]
    distance = np.abs(candidate_points[0] - point_reference)
    for i in range(1, len(candidate_points)):
        if distance > np.abs(candidate_points[i] - point_reference):
            nearest_point_index = i
            nearest_point = candidate_points[i]
            distance = np.abs(candidate_points[i] - point_reference)

    return nearest_point, nearest_point_index


def get_x_values(list_points: list, y_value: float) -> tuple[list, int]:
    """
    Find the x values corresponding to the given y value. The structure of list_points must be like this:
        [(y_value, x_values_list), (y_value, x_values_list), (y_value, x_values_list),...]
    :param list_points: The list of x values and y values
    :param y_value: the y value to compare with
    :return: the list of available x points for y point given and its index
    """
    for i in range(len(list_points)):
        if list_points[i][0] == y_value:
            return list_points[i][1], i


class InLineSeparator(QGraphicsLineItem):
    def __init__(self, x, y, size, parent, fixed_points=None):
        super().__init__(0, 0, 0, size, parent)
        self.setPos(x, y)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIgnoresParentOpacity)

        # If set, itemChange() is called after a movement
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)

        if fixed_points is not None:
            if not isinstance(fixed_points, (np.ndarray, np.generic, list)):
                raise TypeError('fixed_x_points must be a list')
        self.fixed_points = fixed_points

    def set_aux_separator(self, x_list_index, x_index):
        self.parentItem().aux_separator = InLineSeparator(
            self.fixed_points[x_list_index][1][x_index],
            self.fixed_points[x_list_index][0],
            self.line().dy(),
            self.parentItem(),
            self.fixed_points
        )
        self.parentItem().aux_separator.setPen(self.pen())
        self.parentItem().aux_separator.installSceneEventFilter(self.parentItem())

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange and self.scene() is not None:
            y_value, y_value_index = find_nearest_point(
                [i[0] for i in self.fixed_points],
                self.scene().views()[0].mapFromGlobal(QCursor.pos()).y()
            )
            return QPointF(value.x(), y_value)
        return super().itemChange(change, value)

    def mouseReleaseEvent(self, event):
        # Set nearest fixed position
        if self.fixed_points is not None:
            x_list, x_list_index = get_x_values(self.fixed_points, self.pos().y())
            x_value, x_value_index = find_nearest_point(x_list, self.pos().x())
            self.setPos(x_value, self.pos().y())
            if x_value_index == 0 and x_list_index != 0:
                self.set_aux_separator(x_list_index - 1, -1)
            elif x_value_index == len(x_list) - 1 and x_list_index != (len(self.fixed_points) - 1):
                self.set_aux_separator(x_list_index + 1, 0)

        # Execute super function to allow correct object behaviour
        super().mouseReleaseEvent(event)

    def __del__(self):
        print("deleted")


class Separator(QGraphicsLineItem):
    def __init__(self, x, y, size, parent, fixed_points=None):
        super().__init__(0, 0, 0, size, parent)

        self.setOpacity(0)

        self.main_separator = InLineSeparator(x, y, size, self, fixed_points)
        self.main_separator.installSceneEventFilter(self)

        self.setPos(x, y)
        self.aux_separator = None

    def setPos(self, *args) -> None:
        if len(args) == 1 and isinstance(args[0], (QtCore.QPointF, QtCore.QPoint)):
            self.main_separator.setPos(args[0])
        elif len(args) == 2 and all(isinstance(x, (float, int)) for x in args):
            self.main_separator.setPos(args[0], args[1])
        else:
            raise TypeError('TypeError in setPos() function')

    def pos(self) -> QtCore.QPointF:
        return self.main_separator.pos()

    def setPen(self, pen: typing.Union[QtGui.QPen, QtGui.QColor, QtCore.Qt.GlobalColor, QtGui.QGradient]) -> None:
        self.main_separator.setPen(pen)

    def sceneEventFilter(self, watched, event):
        if isinstance(event, QEvent):
            if event.type() == QEvent.GrabMouse:
                if self.aux_separator is watched:
                    self.scene().removeItem(self.main_separator)
                    self.main_separator = self.aux_separator
                    self.aux_separator = None
                if self.main_separator is watched:
                    if self.aux_separator is not None:
                        self.scene().removeItem(self.aux_separator)
                        self.aux_separator = None
        return False

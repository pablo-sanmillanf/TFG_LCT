import typing

import numpy as np
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QPointF, QMutex, QMutexLocker
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsItem, QGraphicsSceneMouseEvent
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
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIgnoresParentOpacity)

        # When position is changed via setPos, change itemChange behaviour
        self.pos_set = False

        self.setPos(x, y)

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

    def setPos(self, *args) -> None:
        self.pos_set = True
        if len(args) == 1 and isinstance(args[0], (QtCore.QPointF, QtCore.QPoint)):
            super().setPos(args[0])
        elif len(args) == 2 and all(isinstance(x, (float, int)) for x in args):
            super().setPos(args[0], args[1])
        else:
            raise TypeError('TypeError in setPos() function')

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange and self.scene() is not None:
            if self.pos_set is False:
                y_value, y_value_index = find_nearest_point(
                    [i[0] for i in self.fixed_points],
                    self.scene().views()[0].mapFromGlobal(QCursor.pos()).y()
                )
                x_value = value.x()
                x_list = get_x_values(self.fixed_points, y_value)[0]
                if x_value < x_list[0]:
                    x_value = x_list[0]
                elif x_value > x_list[-1]:
                    x_value = x_list[-1]
                return QPointF(x_value, y_value)
            self.pos_set = False
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

        # There are several problems of concurrency in the function
        # sceneEventFilter, so this variable is to set sceneEventFilter thread-safe
        self.mutex = QMutex()

        self.setOpacity(0)

        self.main_separator = InLineSeparator(x, y, size, self, fixed_points)
        self.main_separator.installSceneEventFilter(self)

        self.setPos(x, y)
        self.aux_separator = None
        self.watchers = []

    def setPos(self, *args) -> None:
        if len(args) == 1 and isinstance(args[0], (QtCore.QPointF, QtCore.QPoint)):
            req_x = args[0].x()
            req_y = args[0].y()
        elif len(args) == 2 and all(isinstance(x, (float, int)) for x in args):
            req_x = args[0]
            req_y = args[1]
        else:
            raise TypeError('TypeError in setPos() function')

        y_value = find_nearest_point(
            [i[0] for i in self.main_separator.fixed_points],
            req_y
        )[0]
        x_value = find_nearest_point(
            get_x_values(self.main_separator.fixed_points, y_value)[0],
            req_x
        )[0]
        self.main_separator.setPos(x_value, y_value)

    def installSceneEventFilter(self, filterItem: QGraphicsItem) -> None:
        if not (filterItem in self.watchers):
            self.watchers.append(filterItem)
        self.main_separator.installSceneEventFilter(filterItem)

    def pos(self) -> QtCore.QPointF:
        return self.main_separator.pos()

    def setPen(self, pen: typing.Union[QtGui.QPen, QtGui.QColor, QtCore.Qt.GlobalColor, QtGui.QGradient]) -> None:
        self.main_separator.setPen(pen)

    def pen(self) -> QtGui.QPen:
        return self.main_separator.pen()

    def get_y_values(self):
        return [i[0] for i in self.main_separator.fixed_points]

    def get_x_values(self, y_value):
        return get_x_values(self.main_separator.fixed_points, y_value)

    def sceneEventFilter(self, watched, event):
        if isinstance(event, QEvent):
            if event.type() == QEvent.GrabMouse:
                locker = QMutexLocker(self.mutex)
                if self.aux_separator is watched:
                    self.scene().removeItem(self.main_separator)
                    self.main_separator = self.aux_separator
                    self.aux_separator = None
                    for watcher in self.watchers:
                        self.main_separator.installSceneEventFilter(watcher)
                if self.main_separator is watched:
                    if self.aux_separator is not None:
                        self.scene().removeItem(self.aux_separator)
                        self.aux_separator = None
        return False

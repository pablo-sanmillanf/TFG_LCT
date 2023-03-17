from typing import Any

import numpy as np
from PyQt5 import QtCore
from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsItem, QGraphicsSceneMouseEvent


def find_nearest_point(candidate_points: list, point_reference: float) -> float:
    """
    Find the nearest float to point_reference from the list candidate_points.
    :param candidate_points: A list of floats with the possible values
    :param point_reference: The float to compare with
    :return: The nearest float in the list
    """
    return min(candidate_points, key=lambda x: np.abs(x - point_reference))


class Separator(QGraphicsLineItem):
    """
    This class represents a QGraphicsLineItem that can only move between the points contained in the
    fixed_points structure.
    To avoid redundant information this structure must be: [(y_0, [x_0, x_1, ...]), (y_1, [x_0, x_1, ...]), ...]
    """
    def __init__(self, x: float, y: float, size: float,
                 fixed_points: list[tuple[float, list[float]]], parent: QGraphicsItem) -> None:
        """
        Create Separator object. The requested position will be adjusted to the nearest position contained in
        fixed_points
        :param x: X coordinate of the Separator
        :param y: Y coordinate of the Separator
        :param size: The height of the Separator
        :param fixed_points: fixed_points: Available points for the separators. The structure must
                             be [(y_0, [x_0, x_1, ...]), (y_1, [x_0, x_1, ...]), ...]
        :param parent: The QGraphicsItem parent of this Separator. Can't be None
        """
        super().__init__(0, 0, 0, size, parent)

        self.setFlags(QGraphicsItem.ItemIsMovable |
                      QGraphicsItem.ItemIgnoresParentOpacity |
                      QGraphicsItem.ItemSendsGeometryChanges)  # If set, itemChange() is called after a movement

        self.setCursor(Qt.SplitHCursor)

        # When position is changed via setPos, change itemChange behaviour
        self.pos_set = False

        if not isinstance(fixed_points, (np.ndarray, np.generic, list)):
            raise TypeError('fixed_x_points must be a list')
        self.fixed_points = fixed_points

        self.setPos(x, y)

    def get_y_values(self):
        """
        Return y values from self.fixed_points structure
        :return: the list of available y points
        """
        return [i[0] for i in self.fixed_points]

    def get_x_values(self, y_value: float) -> list:
        """
        Find the x values corresponding to the given y value from self.fixed_points
        :param y_value: the y value to compare with
        :return: the list of available x points for y point given
        """
        for tuple_point in self.fixed_points:
            if tuple_point[0] == y_value:
                return tuple_point[1]

    def setPos(self, *args) -> None:
        """
        Set position of the Separator. The requested position will be adjusted to the nearest position
        contained in fixed_points
        :param args: The position, structured as a QPointF or a list with two elements (x and y)
        """
        self.pos_set = True
        if len(args) == 1 and isinstance(args[0], (QtCore.QPointF, QtCore.QPoint)):
            req_x = args[0].x()
            req_y = args[0].y()
        elif len(args) == 2 and all(isinstance(x, (float, int)) for x in args):
            req_x = args[0]
            req_y = args[1]
        else:
            raise TypeError('TypeError in setPos() function')

        y_value = find_nearest_point(self.get_y_values(), req_y)
        x_value = find_nearest_point(self.get_x_values(y_value), req_x)
        super().setPos(x_value, y_value)

    def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value: Any) -> QPointF:
        """
        Manages the changes associated to the Separator. In the case of the Separator,
        only position changes will be treated
        :param change: The object that indicates the type of event change triggered
        :param value: An object associated with this change. In our case, this will be
                      the requested position of the element
        :return: The position to be placed
        """
        if change == QGraphicsItem.ItemPositionChange and self.scene() is not None:
            if self.pos_set is False:
                y_value = find_nearest_point(
                    self.get_y_values(),
                    self.scene().views()[0].mapFromGlobal(QCursor.pos()).y()
                )
                x_value = value.x()
                x_list = self.get_x_values(y_value)
                if x_value < x_list[0]:
                    x_value = x_list[0]
                elif x_value > x_list[-1]:
                    x_value = x_list[-1]
                return QPointF(x_value, y_value)
            else:
                self.pos_set = False
        return super().itemChange(change, value)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        """
        Manages the behaviour of the Separator when the user release the object. In this case, the object goes
        automatically to the nearest allowed position.
        :param event: The object that indicates the type of event triggered. In this case is a QGraphicsSceneMouseEvent
        """
        # Set nearest fixed position
        if self.fixed_points is not None:
            y_value = find_nearest_point(self.get_y_values(), self.pos().y())
            x_value = find_nearest_point(self.get_x_values(y_value), self.pos().x())
            self.setPos(x_value, y_value)

        # Execute super function to allow correct object behaviour
        super().mouseReleaseEvent(event)

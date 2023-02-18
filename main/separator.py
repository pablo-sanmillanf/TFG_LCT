import numpy as np
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsItem


def find_nearest_point(candidate_points: list, point_reference: float) -> float:
    """
    Find the nearest float to point_reference from the list candidate_points.
    :param candidate_points: A list of floats with the possible values
    :param point_reference: The float to compare with
    :return: The nearest float
    """
    return min(candidate_points, key=lambda x: np.abs(x - point_reference))


def get_x_values(list_points: list, y_value: float) -> list:
    """
    Find the x values corresponding to the given y value. The structure of list_points will be like this:
        [(y_value, x_values_list), (y_value, x_values_list), (y_value, x_values_list),...]
    :param list_points: The list of x values and y values
    :param y_value: the y value to compare with
    :return: the list of available x points for y point given
    """
    for tuple_point in list_points:
        if tuple_point[0] == y_value:
            return tuple_point[1]


class CustomSeparator(QGraphicsLineItem):
    def __init__(self, x, y, size, parent, fixed_points=None):
        super().__init__(x, y, x, y + size, parent)
        self.setFlag(QGraphicsItem.ItemIsMovable)

        # If set, itemChange() is called after a movement
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)

        if fixed_points is not None:
            if not isinstance(fixed_points, (np.ndarray, np.generic, list)):
                raise TypeError('fixed_x_points must be a list')
        self.fixed_points = fixed_points

    def itemChange(self, change, value):

        if change == QGraphicsItem.ItemPositionChange:
            point = QPointF(
                value.x(),
                find_nearest_point(
                    [i[0] for i in self.fixed_points],
                    self.scene().views()[0].mapFromGlobal(QCursor.pos()).y()
                )
            )
            return point
        return super().itemChange(change, value)

    def mouseReleaseEvent(self, event):
        # Set nearest fixed position
        if self.fixed_points is not None:
            self.setPos(QPointF(
                find_nearest_point(
                    get_x_values(
                        self.fixed_points,
                        self.pos().y()
                    ),
                    self.pos().x()
                ),
                self.pos().y())
            )

        # Execute super function to allow correct object behaviour
        super().mouseReleaseEvent(event)

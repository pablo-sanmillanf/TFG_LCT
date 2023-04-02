import typing
from typing import Any

import numpy as np
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QPointF, Qt, QRectF
from PyQt5.QtGui import QCursor, QPainterPath
from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsItem, QGraphicsSceneMouseEvent, QWidget, \
    QStyleOptionGraphicsItem


def find_nearest_point(candidate_points: list[float], point_reference: float) -> float:
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
    border_right_pos: bool
    border_left_pos: bool
    size: QRectF

    def __init__(self, x: float, y: float, height: float,
                 fixed_points: list[tuple[float, list[float]]], parent: QGraphicsItem) -> None:
        """
        Create Separator object. The requested position will be adjusted to the nearest position contained in
        fixed_points
        :param x: X coordinate of the Separator
        :param y: Y coordinate of the Separator
        :param height: The height of the Separator
        :param fixed_points: fixed_points: Available points for the separators. The structure must
                             be [(y_0, [x_0, x_1, ...]), (y_1, [x_0, x_1, ...]), ...]
        :param parent: The QGraphicsItem parent of this Separator. Can't be None
        """
        super().__init__(0, 0, 0, height, parent)
        self.setZValue(2)
        self.border_left_pos = False
        self.border_right_pos = False
        self.size = QRectF(0, 0, 0, 0)
        self.height = height

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

    def set_height(self, height: float | int) -> None:
        """
        Change height of the Separator object.
        :param height: Height in pixels.
        """
        self.height = height
        self.setLine(0, 0, 0, height)

    def set_bounding_rect(self) -> None:
        """
        Set the bounding rect. If the item is not in the border, the bounding rect is the regular bounding rect.
        If it is on the border, modify the bounding rect to span the original and the copy created at the beginning
        of the next row (if the original was at the end of the line) or at the end of the previous row (if the
        original was at the beginning of the line).
        """
        if self.border_left_pos and not self.border_right_pos:
            y_values = self.get_y_values()
            y_value_previous_line = y_values[y_values.index(self.pos().y()) - 1]
            x_values_previous_line = self.get_x_values(y_value_previous_line)
            self.prepareGeometryChange()  # Has to be called before bounding rect updating
            self.size = QRectF(
                -self.pen().widthF() / 2,
                y_value_previous_line - self.pos().y(),
                x_values_previous_line[-1] - self.pos().x() + self.pen().widthF(),
                self.pos().y() - y_value_previous_line + self.height
            )

        elif not self.border_left_pos and self.border_right_pos:
            y_values = self.get_y_values()
            y_value_next_line = y_values[y_values.index(self.pos().y()) + 1]
            x_values_next_line = self.get_x_values(y_value_next_line)
            self.prepareGeometryChange()  # Has to be called before bounding rect updating
            self.size = QRectF(
                -self.pen().widthF() / 2 + x_values_next_line[0] - self.pos().x(),
                0,
                self.pos().x() - x_values_next_line[0] + self.pen().widthF(),
                y_value_next_line - self.pos().y() + self.height
            )

    def is_on_the_border(self) -> bool:
        """
        Return True if the element is on the border of a line.
        :return: True if is on the border.
        """
        return self.border_left_pos or self.border_right_pos

    def complete_pos(self, left_pos: bool) -> QtCore.QPointF:
        """
        Return element position as a QPointF. If the element is on the border, depending on the value of left_pos,
        this function will return one position or another. If it is True, it will return left border element position.
        If it is False, it will return right border element position. If the element is not on the border, left_pos
        don't care. This function should be called instead of pos().
        :param left_pos: A boolean that indicates which position should be returned. True, if left border element
                         position, False if right border element position.
        :return: Element position.
        """
        if not self.border_left_pos and not self.border_right_pos:
            return self.pos()
        elif self.border_left_pos and not self.border_right_pos:
            if left_pos:
                return self.pos()
            else:
                y_values = self.get_y_values()
                y_value_previous_line = y_values[y_values.index(self.pos().y()) - 1]
                return QPointF(
                    self.get_x_values(y_value_previous_line)[-1],
                    y_value_previous_line
                )
        elif not self.border_left_pos and self.border_right_pos:
            if left_pos:
                y_values = self.get_y_values()
                y_value_next_line = y_values[y_values.index(self.pos().y()) + 1]
                return QPointF(
                    self.get_x_values(y_value_next_line)[0],
                    y_value_next_line
                )
            else:
                return self.pos()

    def setPen(self, pen: typing.Union[QtGui.QPen, QtGui.QColor, QtCore.Qt.GlobalColor, QtGui.QGradient]) -> None:
        """
        Sets a pen style to the Separator.
        :param pen: The QPen object.
        """
        super().setPen(pen)
        if self.is_on_the_border():
            self.set_bounding_rect()

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

        y_list_values = self.get_y_values()
        y_value = find_nearest_point(self.get_y_values(), req_y)

        x_list_values = self.get_x_values(y_value)
        x_value = find_nearest_point(self.get_x_values(y_value), req_x)
        super().setPos(x_value, y_value)

        if x_list_values.index(x_value) == 0 and y_list_values.index(y_value) > 0:
            self.border_left_pos = True
            self.set_bounding_rect()
        elif x_list_values.index(x_value) == len(x_list_values) - 1 and \
                y_list_values.index(y_value) < len(y_list_values) - 1:
            self.border_right_pos = True
            self.set_bounding_rect()
        elif self.border_left_pos:
            self.prepareGeometryChange()  # Has to be called before bounding rect updating
            self.border_left_pos = False
        elif self.border_right_pos:
            self.prepareGeometryChange()  # Has to be called before bounding rect updating
            self.border_right_pos = False

    def shape(self) -> QPainterPath:
        """
        Returns a QPainterPath with the zones within the bounding rect that can be selected for further editing
        of the text. Each of these zones represents a rectangle that covers the text in one line.
        :return: A QPainterPath with the custom shape
        """
        path = super().shape()
        if not self.border_left_pos and not self.border_right_pos:
            return path
        elif self.border_left_pos and not self.border_right_pos:
            path.addRect(
                QRectF(
                    self.boundingRect().width() - self.pen().widthF(),
                    self.height - self.boundingRect().height(),
                    self.boundingRect().width(),
                    self.height
                    )
            )
            return path
        elif not self.border_left_pos and self.border_right_pos:
            path.addRect(
                QRectF(
                    -self.boundingRect().width() + self.pen().widthF(),
                    self.boundingRect().height() - self.height,
                    -self.boundingRect().width() + 2 * self.pen().widthF(),
                    self.boundingRect().height()
                )
            )
            return path

        raise RuntimeError("Problems with custom shape in Separator object")

    def boundingRect(self) -> QRectF:
        """
        Returns the bounding rect that occupies the element.
        :return: The bounding rect as a QRectF
        """
        if not self.border_left_pos and not self.border_right_pos:
            return super().boundingRect()
        elif (self.border_left_pos and not self.border_right_pos) or \
                (not self.border_left_pos and self.border_right_pos):
            return self.size
        else:
            raise RuntimeError("Problems with custom bounding rect in Separator object")

    def paint(self,
              painter: QtGui.QPainter,
              option: "QStyleOptionGraphicsItem",
              widget: typing.Optional[QWidget] = ...) -> None:
        """
        Paints the separator using the information stored in self.fixed_points.
        :param painter: The object to paint the rectangles in the canvas
        :param option: This parameter will be ignored
        :param widget: This parameter will be ignored
        """
        super().paint(painter, option, widget)
        if self.border_left_pos and not self.border_right_pos:
            painter.translate(
                QPointF(
                    self.boundingRect().width() - self.pen().widthF(),
                    self.height - self.boundingRect().height()
                )
            )
            super().paint(painter, option, widget)
        elif not self.border_left_pos and self.border_right_pos:
            painter.translate(
                QPointF(
                    -self.boundingRect().width() + self.pen().widthF(),
                    self.boundingRect().height() - self.height
                )
            )
            super().paint(painter, option, widget)

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
                    self.parentItem().mapFromScene(self.scene().views()[0].mapFromGlobal(QCursor.pos())).y() +
                    self.scene().views()[0].verticalScrollBar().value()
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

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        """
        Manages the behaviour of the Separator when the user release the object. In this case, the object changes its
        bounding rect if self.border_left_pos or self.border_right_pos are active.
        :param event: The object that indicates the type of event triggered. In this case is a QGraphicsSceneMouseEvent
        """
        if self.border_left_pos and not self.border_right_pos:
            cursor_pos = self.parentItem().mapFromScene(self.scene().views()[0].mapFromGlobal(QCursor.pos()))
            self.setPos(cursor_pos.x(), cursor_pos.y() + self.scene().views()[0].verticalScrollBar().value())
            self.prepareGeometryChange()  # Has to be called before bounding rect updating
            self.border_left_pos = False
        elif not self.border_left_pos and self.border_right_pos:
            cursor_pos = self.parentItem().mapFromScene(self.scene().views()[0].mapFromGlobal(QCursor.pos()))
            self.setPos(cursor_pos.x(), cursor_pos.y() + self.scene().views()[0].verticalScrollBar().value())
            self.prepareGeometryChange()  # Has to be called before bounding rect updating
            self.border_right_pos = False
        elif self.border_left_pos and self.border_right_pos:
            raise RuntimeError("Problems with mousePressEvent in Separator object")
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        """
        Manages the behaviour of the Separator when the user release the object. In this case, the object goes
        automatically to the nearest allowed position.
        :param event: The object that indicates the type of event triggered. In this case is a QGraphicsSceneMouseEvent
        """
        # Set nearest fixed position
        self.setPos(self.pos())

        # Execute super function to allow correct object behaviour
        super().mouseReleaseEvent(event)

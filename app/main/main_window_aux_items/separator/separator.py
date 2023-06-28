import typing
from typing import Any

import numpy as np
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QPointF, Qt, QRectF, pyqtSignal, QObject, QMutex, QMutexLocker
from PyQt5.QtGui import QCursor, QPainterPath
from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsItem, QGraphicsSceneMouseEvent, QWidget, \
    QStyleOptionGraphicsItem


def find_nearest_point(candidate_points: list[float] | tuple[float] | list[tuple[float, bool]], point_reference: float,
                       ) -> float:
    """
    Find the nearest float to point_reference from the list candidate_points.
    :param candidate_points: A list of floats with the possible values. If the list is of type list[tuple[float, bool]],
                             the boolean indicates if the point has to be ignored in the finding.
    :param point_reference: The float to compare with
    :return: The nearest float in the list
    """
    if all(isinstance(item, tuple) for item in candidate_points):
        return min(
            candidate_points,
            key=lambda x: 1000000 if x[1] else np.abs(x[0] - point_reference)
        )[0]
    else:
        return min(candidate_points, key=lambda x: np.abs(x - point_reference))


class SeparatorEmitter(QObject):
    # (Separator_created, Point_of_separator)
    created = pyqtSignal(QGraphicsLineItem, QPointF)

    # (Separator_moved, Point_of_separator)
    pos_changed = pyqtSignal(QGraphicsLineItem, QPointF)

    # (Separator_released)
    released = pyqtSignal(QGraphicsLineItem)

    # (Separator_clicked, Cursor_point, Right_point_of_separator, Left_point_of_separator)
    clicked_on_the_border = pyqtSignal(QGraphicsLineItem, QPointF, QPointF, QPointF)

    # (Separator_removed)
    removed = pyqtSignal(QGraphicsLineItem)


class Separator(QGraphicsLineItem):
    """
    This class represents a QGraphicsLineItem that can only move between the points contained in the fixed_points
    structure. If the "Ignored" boolean is True, the separator cannot release in this point. If the separator is
    released in the border of a line, a copy of it appears at the end of the previous line (if it is on the left border)
    or at the beginning of the next line (if it is on the right border) and both copies are also selectable.
    To avoid redundant information this structure must be:
    [(y_0, [(x_0, Ignored), (x_1, Ignored), ...]), (y_1, [(x_0, Ignored), (x_1, Ignored), ...]), ...]
    """
    _fixed_points: list[tuple[float, list[tuple[float, bool]]]]
    _border_right_pos: bool
    _border_left_pos: bool
    _size: QRectF

    def __init__(self, x: float, y: float, height: float, fixed_points: list[tuple[float, list[tuple[float, bool]]]],
                 emitter: SeparatorEmitter, parent: QGraphicsItem) -> None:
        """
        Create Separator object. The requested position will be adjusted to the nearest position contained in
        fixed_points
        :param x: X coordinate of the Separator
        :param y: Y coordinate of the Separator
        :param height: The height of the Separator
        :param fixed_points: Available points for the separators. The structure must be
                            [
                            (y_0, [(x_0, Ignored), (x_1, Ignored), ...]),
                            (y_1, [(x_0, Ignored), (x_1, Ignored), ...]),
                            ...
                            ]
        :param emitter: The QObject that will handle the signals that will emit the Separator.
        :param parent: The QGraphicsItem parent of this Separator. Can't be None
        """
        self._is_clicked = False
        self._mutex = QMutex()

        self._emitter = emitter

        super().__init__(0, 0, 0, height, parent)
        self.setZValue(2)
        self._border_left_pos = False
        self._border_right_pos = False
        self._size = QRectF(0, 0, 0, 0)
        self._height = height
        self.first_time = True

        self.setFlags(QGraphicsItem.ItemIsMovable |
                      QGraphicsItem.ItemIgnoresParentOpacity |
                      QGraphicsItem.ItemSendsGeometryChanges)  # If set, itemChange() is called after a movement

        self.setCursor(Qt.SplitHCursor)

        # When position is changed via setPos, change itemChange behaviour
        self._pos_set = False

        self._fixed_points = fixed_points

        self.setPos(x, y)

    def set_fixed_points(self, fixed_points: list[tuple[float, list[tuple[float, bool]]]]) -> None:
        """
        Sets the point structure through which the Separator can be moved.
        """
        self._fixed_points = fixed_points

    def _get_y_values(self):
        """
        Return y values from self.fixed_points structure
        :return: the list of available y points
        """
        return [i[0] for i in self._fixed_points]

    def _get_x_values(self, y_value: float) -> list[float]:
        """
        Find the x values corresponding to the given y value from self.fixed_points
        :param y_value: the y value to compare with
        :return: the list of available x points for y point given
        """
        for tuple_point in self._fixed_points:
            if tuple_point[0] == y_value:
                return [i[0] for i in tuple_point[1]]

    def _get_x_values_with_complete_info(self, y_value: float) -> list[tuple[float, bool]]:
        """
        Find the x values corresponding to the given y value from self.fixed_points and return a tuple array
        with the x_values and a boolean that indicates if the separator can be released in this position (False) or
        not (True).
        :param y_value: the y value to compare with
        :return: the list of available x points for y point given
        """
        for tuple_point in self._fixed_points:
            if tuple_point[0] == y_value:
                return tuple_point[1]

    def set_height(self, height: float | int) -> None:
        """
        Change height of the Separator object.
        :param height: Height in pixels.
        """
        self._height = height
        self.setLine(0, 0, 0, height)

    def _set_bounding_rect(self) -> None:
        """
        Set the bounding rect. If the item is not in the border, the bounding rect is the regular bounding rect.
        If it is on the border, modify the bounding rect to span the original and the copy created at the beginning
        of the next row (if the original was at the end of the line) or at the end of the previous row (if the
        original was at the beginning of the line).
        """
        if self._border_left_pos and not self._border_right_pos:
            y_values = self._get_y_values()
            y_value_previous_line = y_values[y_values.index(self.pos().y()) - 1]
            x_values_previous_line = self._get_x_values(y_value_previous_line)
            self.prepareGeometryChange()  # Has to be called before bounding rounded_rect updating
            self._size = QRectF(
                -self.pen().widthF() / 2,
                y_value_previous_line - self.pos().y(),
                x_values_previous_line[-1] - self.pos().x() + self.pen().widthF(),
                self.pos().y() - y_value_previous_line + self._height
            )

        elif not self._border_left_pos and self._border_right_pos:
            y_values = self._get_y_values()
            y_value_next_line = y_values[y_values.index(self.pos().y()) + 1]
            x_values_next_line = self._get_x_values(y_value_next_line)
            self.prepareGeometryChange()  # Has to be called before bounding rounded_rect updating
            self._size = QRectF(
                -self.pen().widthF() / 2 + x_values_next_line[0] - self.pos().x(),
                0,
                self.pos().x() - x_values_next_line[0] + self.pen().widthF(),
                y_value_next_line - self.pos().y() + self._height
            )

    def _emit_pos_changed(self) -> None:
        """
        This function is used to notify the position of the Separator. It's an internal function. If the use of this
        function is needed externally, should be called when the Separator is not moving.
        """
        if self._emitter is not None:
            self._emitter.pos_changed.emit(self, self.pos())

    def _emit_created(self) -> None:
        """
        This function is used to notify the position of the Separator. It's an internal function. If the use of this
        function is needed externally, should be called when the Separator is not moving.
        """
        if self._emitter is not None:
            self._emitter.created.emit(self, self.pos())

    def _emit_clicked_on_the_border(self, cursor_pos: QPointF) -> None:
        """
        This function is used to notify the position of the Separator and the cursor when the Separator is clicked on
        the border. It's an internal function. If the use of this function is needed externally, should be called when
        the Separator is not moving.
        """
        if self._emitter is not None:
            lock = QMutexLocker(self._mutex)
            self._emitter.clicked_on_the_border.emit(
                self, cursor_pos, self.complete_pos(False), self.complete_pos(True)
            )

    def is_on_the_border(self) -> bool:
        """
        Return True if the element is on the border of a line.
        :return: True if is on the border.
        """
        return self._border_left_pos or self._border_right_pos

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
        if not self._border_left_pos and not self._border_right_pos:
            return self.pos()
        elif self._border_left_pos and not self._border_right_pos:
            if left_pos:
                return self.pos()
            else:
                y_values = self._get_y_values()
                y_value_previous_line = y_values[y_values.index(self.pos().y()) - 1]
                return QPointF(
                    self._get_x_values(y_value_previous_line)[-1],
                    y_value_previous_line
                )
        elif not self._border_left_pos and self._border_right_pos:
            if left_pos:
                y_values = self._get_y_values()
                y_value_next_line = y_values[y_values.index(self.pos().y()) + 1]
                return QPointF(
                    self._get_x_values(y_value_next_line)[0],
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
            self._set_bounding_rect()

    def setPos(self, *args: typing.Union[QPointF, float, float]) -> None:
        """
        Set position of the Separator. The requested position will be adjusted to the nearest position
        contained in fixed_points
        :param args: The position, structured as a QPointF or a list with two elements (x and y)
        """
        self._pos_set = True
        if len(args) == 1:
            req_x = args[0].x()
            req_y = args[0].y()
        else:
            req_x = args[0]
            req_y = args[1]

        y_list_values = self._get_y_values()
        y_value = find_nearest_point(y_list_values, req_y)

        x_list_values = self._get_x_values_with_complete_info(y_value)
        x_value = find_nearest_point(x_list_values, req_x)

        x_index = [i[0] for i in x_list_values].index(x_value)
        y_index = y_list_values.index(y_value)

        super().setPos(x_value, y_value)
        if not self._is_clicked and x_index == 0 and y_index > 0:
            self._border_left_pos = True
            self._border_right_pos = False
            self._set_bounding_rect()
        elif not self._is_clicked and x_index == len(x_list_values) - 1 and y_index < len(y_list_values) - 1:
            self._border_right_pos = True
            self._border_left_pos = False
            self._set_bounding_rect()
        elif self._border_left_pos:
            self.prepareGeometryChange()  # Has to be called before bounding rounded_rect updating
            self._border_left_pos = False
        elif self._border_right_pos:
            self.prepareGeometryChange()  # Has to be called before bounding rounded_rect updating
            self._border_right_pos = False

    def shape(self) -> QPainterPath:
        """
        Returns a QPainterPath with the zones within the bounding rounded_rect that can be selected for further editing
        of the text. Each of these zones represents a rectangle that covers the text in one line.
        :return: A QPainterPath with the custom shape
        """
        path = super().shape()
        if not self._border_left_pos and not self._border_right_pos:
            return path
        elif self._border_left_pos and not self._border_right_pos:
            path.addRect(
                QRectF(
                    self.boundingRect().width() - self.pen().widthF(),
                    self._height - self.boundingRect().height(),
                    self.boundingRect().width(),
                    self._height
                )
            )
            return path
        elif not self._border_left_pos and self._border_right_pos:
            path.addRect(
                QRectF(
                    -self.boundingRect().width() + self.pen().widthF(),
                    self.boundingRect().height() - self._height,
                    -self.boundingRect().width() + 2 * self.pen().widthF(),
                    self.boundingRect().height()
                )
            )
            return path

        raise RuntimeError("Problems with custom shape in Separator object")

    def boundingRect(self) -> QRectF:
        """
        Returns the bounding rounded_rect that occupies the element.
        :return: The bounding rounded_rect as a QRectF
        """
        if not self._border_left_pos and not self._border_right_pos:
            return super().boundingRect()
        elif (self._border_left_pos and not self._border_right_pos) or \
                (not self._border_left_pos and self._border_right_pos):
            return self._size
        else:
            raise RuntimeError("Problems with custom bounding rounded_rect in Separator object")

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
        if self._border_left_pos and not self._border_right_pos:
            painter.translate(
                QPointF(
                    self.boundingRect().width() - self.pen().widthF(),
                    self._height - self.boundingRect().height()
                )
            )
            super().paint(painter, option, widget)
        elif not self._border_left_pos and self._border_right_pos:
            painter.translate(
                QPointF(
                    -self.boundingRect().width() + self.pen().widthF(),
                    self.boundingRect().height() - self._height
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
        lock = QMutexLocker(self._mutex)
        if self.scene() is not None:
            if change == QGraphicsItem.ItemPositionChange:
                if self._pos_set is False:
                    y_value = find_nearest_point(
                        self._get_y_values(),
                        self.parentItem().mapFromScene(self.scene().views()[0].mapFromGlobal(QCursor.pos())).y() +
                        self.scene().views()[0].verticalScrollBar().value()
                    )
                    x_value = value.x()
                    x_list = self._get_x_values(y_value)
                    if x_value < x_list[0]:
                        x_value = x_list[0]
                    elif x_value > x_list[-1]:
                        x_value = x_list[-1]
                    return QPointF(x_value, y_value)
                else:
                    self._pos_set = False
            elif change == QGraphicsItem.ItemPositionHasChanged:
                if self.first_time:
                    self.first_time = False
                    self._emit_created()
                else:
                    self._emit_pos_changed()
        return super().itemChange(change, value)

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        """
        Manages the behaviour of the Separator when the user release the object. In this case, the object changes its
        bounding rect if self.border_left_pos or self.border_right_pos are active.
        :param event: The object that indicates the type of event triggered. In this case is a QGraphicsSceneMouseEvent
        """
        self._is_clicked = True
        if self._border_left_pos and not self._border_right_pos:

            # Obtain cursor position
            cursor_pos = self.parentItem().mapFromScene(self.scene().views()[0].mapFromGlobal(QCursor.pos()))

            # Emit signal with the cursor position and the left and right position
            self._emit_clicked_on_the_border(cursor_pos)

            # Change Separator position to match with the cursor position
            self.setPos(cursor_pos.x(), cursor_pos.y() + self.scene().views()[0].verticalScrollBar().value())

            # Change bounding rounded_rect
            self.prepareGeometryChange()  # Has to be called before bounding rounded_rect updating
            self._border_left_pos = False

        elif not self._border_left_pos and self._border_right_pos:

            # Obtain cursor position
            cursor_pos = self.parentItem().mapFromScene(self.scene().views()[0].mapFromGlobal(QCursor.pos()))

            # Emit signal with the cursor position and the left and right position
            self._emit_clicked_on_the_border(cursor_pos)

            # Change Separator position to match with the cursor position
            self.setPos(cursor_pos.x(), cursor_pos.y() + self.scene().views()[0].verticalScrollBar().value())

            # Change bounding rounded_rect
            self.prepareGeometryChange()  # Has to be called before bounding rounded_rect updating
            self._border_right_pos = False

        elif self._border_left_pos and self._border_right_pos:
            raise RuntimeError("Problems with mousePressEvent in Separator object")
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        """
        Manages the behaviour of the Separator when the user release the object. In this case, the object goes
        automatically to the nearest allowed position.
        :param event: The object that indicates the type of event triggered. In this case is a QGraphicsSceneMouseEvent
        """
        self._is_clicked = False
        # Set nearest fixed position
        self.setPos(self.pos())

        # Execute super function to allow correct object behaviour
        super().mouseReleaseEvent(event)

        if self._emitter is not None:
            self._emitter.released.emit(self)

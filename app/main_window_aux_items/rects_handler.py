import typing
from PyQt5.QtGui import QColor

from .separator import Separator

from PyQt5.QtCore import QPointF
from PyQt5.QtWidgets import (
    QGraphicsRectItem,
    QWidget,
    QStyleOptionGraphicsItem,
    QGraphicsItem,
)
from PyQt5 import QtGui


class RoundedRect(QGraphicsRectItem):
    """
    This class represents a multiple QGraphicsRectItem with rounded corners. It adjusts his line_height and
    the number of QGraphicsRectItem to fill the gap between the associated Separators.
    Assuming the "|" are the separators and the "=" are the rectangles, this is more or less what it will look like:
    |=====================================================================
    ======================================================================
    ====================================|
    """

    def __init__(self, x: float | int, y: float | int, width: float | int, height: float | int, radius: float | int,
                 parent: QGraphicsItem) -> None:
        """
        Create RoundedRect object.
        :param x: The x-position of the rectangle
        :param y: The y-position of the rectangle
        :param width: The width of this element. Is determined by the max text width.
        :param height: The height of the rectangles.
        :param radius: The radius of the rounded corners.
        :param parent: The QGraphicsItem parent of this Separator. Can't be None
        """
        super().__init__(0, 0, width, height, parent)
        self.setPos(x, y)
        self.radius = radius
        self.setFlag(QGraphicsItem.ItemIgnoresParentOpacity)

    def set_background_color(self, color: str) -> None:
        """
        Set the rectangle background color
        :param color: The color as string. Should be a valid HTML color.
        """
        self.setBrush(QColor(color))
        self.update()

    def set_pos_and_size(self, x: float | int, y: float | int, width: float | int, height: float | int):
        """
        Set the position and the size of the rect.
        :param x: The x-position of the rectangle.
        :param y: The y-position of the rectangle.
        :param width: The width of this element.
        :param height: The height of the rectangle.
        """
        self.setRect(0, 0, width, height)
        self.setPos(x, y)

    def paint(self,
              painter: QtGui.QPainter,
              option: "QStyleOptionGraphicsItem",
              widget: typing.Optional[QWidget] = ...) -> None:
        """
        Paints the rectangle with a given radius.
        :param painter: The object to paint the rectangles in the canvas
        :param option: This parameter will be ignored
        :param widget: This parameter will be ignored
        """
        if self.rect().width() != 0:
            painter.setBrush(self.brush())
            painter.drawRoundedRect(self.boundingRect(), self.radius, self.radius)


class RectsHandler:
    """
    This class represents a multiple QGraphicsRectItem with rounded corners. It adjusts his line_height and
    the number of QGraphicsRectItem to fill the gap between the associated Separators.
    Assuming the "|" are the separators and the "=" are the rectangles, this is more or less what it will look like:
    |=====================================================================
    ======================================================================
    ====================================|
    """
    separators: list[list[Separator | int | QPointF | bool]]
    points: list[tuple[float | int, tuple[float | int, float | int]]]
    colors: dict[str, str]

    def __init__(self, height: float | int, radius: float | int,
                 points: list[tuple[float | int, tuple[float | int, float | int]]], parent: QGraphicsItem) -> None:
        """
        Create MultilineRoundedRect object.
        :param height: The height of the rectangles
        :param radius: The radius of the rounded corners
        :param points: The space between the border of a separator and
        :param parent: The QGraphicsItem parent of this Separator. Can't be None
        """
        self.height = height
        self.radius = radius
        self.points = points
        self.parent = parent
        self.rects = []

        for line in points:
            self.rects.append(RoundedRect(line[1][0], line[0], line[1][1] - line[1][0], height, radius, parent))

        self.separators = []

        """self.colors = colors
        self.editable_text_changed_slot([])"""

    def add_separator_listeners(self, pos_changed_fn: typing.Any, clicked_on_the_border_fn: typing.Any) -> None:
        pos_changed_fn.connect(self.separator_position_changed)
        clicked_on_the_border_fn.connect(self.separator_clicked_on_the_border)

    def update_points(self) -> None:
        """
        Updates the points to place the rectangles when both separators have been moved at the same time, e.g. when
        resizing the window.
        """
        pass

    def set_colors(self, colors: dict[str, str]) -> None:
        """
        Set the colors that will be used by the rounded rect depending on the value of the associated descriptor. The
        length of this dict should be the same as the possible combinations of the descriptor text plus one (the default
        one). Also, the colors list should be of any HTML valid color.
        :param colors: Dict of all available colors and the possibilities for the descriptor
        """
        """self.colors = colors
        self.setBrush(QColor(list(self.colors.values())[self.color_index]))
        self.update()"""
        pass

    def find_separator(self, separator: Separator) -> int:
        for i in range(len(self.separators)):
            if self.separators[i][0] is separator:
                return i

    def add_separator(self, separator: Separator, point: QPointF):
        if len(self.separators) == 0:
            self.separators.append([separator, self.insert_rect(point), point])
        else:
            for i in range(len(self.separators)):
                if (point.y() > self.separators[i][0].pos().y() or
                        (point.y() == self.separators[i][0].pos().y() and
                         point.x() > self.separators[i][0].pos().x())):
                    # [Separator, Last_index_before, Last_position]
                    self.separators.insert(i + 1, [separator, self.insert_rect(point), point])

                    # Update "Last_index_before" for the separators after this separator
                    for e in range(i + 2, len(self.separators)):
                        self.separators[e][1] += 1
                    return

            # If the separator is inserted after the first immobile separator
            self.separators.insert(0, [separator, self.insert_rect(point), point])

            # Update "Last_index_before" for the separators after this separator
            for e in range(1, len(self.separators)):
                self.separators[e][1] += 1

    def insert_rect(self, point: QPointF):
        for i in range(len(self.rects)):
            if (point.y() < self.rects[i].pos().y() or
                    (point.y() == self.rects[i].pos().y() and point.x() < self.rects[i].pos().x())):
                self.rects.insert(i, RoundedRect(
                    point.x(),
                    point.y(),
                    self.rects[i - 1].rect().width() + self.rects[i - 1].pos().x() - point.x(),
                    self.height,
                    self.radius,
                    self.parent
                ))

                self.rects[i - 1].set_pos_and_size(
                    self.rects[i - 1].pos().x(),
                    self.rects[i - 1].pos().y(),
                    point.x() - self.rects[i - 1].pos().x(),
                    self.height
                )
                return i - 1

    def update_downwards(self, index, point: QPointF):
        for i in range(index, len(self.rects)):
            if point.y() > self.rects[i].pos().y():
                self.rects[i].set_pos_and_size(
                    self.rects[i].pos().x(),
                    self.rects[i].pos().y(),
                    self.rects[i].rect().width() + self.rects[i + 1].rect().width(),
                    self.height
                )
                self.rects[i + 1].set_pos_and_size(self.rects[i + 2].pos().x(), self.rects[i + 2].pos().y(), 0, 0)
            else:
                self.rects[i + 1].set_pos_and_size(
                    point.x(),
                    self.rects[i].pos().y(),
                    self.rects[i + 1].rect().width() + self.rects[i + 1].pos().x() - point.x(),
                    self.height
                )
                self.rects[i].set_pos_and_size(
                    self.rects[i].pos().x(),
                    self.rects[i].pos().y(),
                    point.x() - self.rects[i].pos().x(),
                    self.height
                )
                return i
        raise RuntimeError("DOWNWARDS FINISH WITHOUT RETURNING")

    def update_upwards(self, index, point: QPointF):
        for i in range(index, -1, -1):
            if point.y() < self.rects[i].pos().y():
                self.rects[i + 1].set_pos_and_size(
                    self.rects[i].pos().x(),
                    self.rects[i].pos().y(),
                    self.rects[i].rect().width() + self.rects[i + 1].rect().width(),
                    self.height
                )
                self.rects[i].set_pos_and_size(
                    self.rects[i - 1].pos().x(),
                    self.rects[i - 1].pos().y(),
                    self.rects[i - 1].rect().width(),
                    self.height
                )
            else:

                self.rects[i + 1].set_pos_and_size(
                    point.x(),
                    self.rects[i].pos().y(),
                    self.rects[i + 1].rect().width() + self.rects[i + 1].pos().x() - point.x(),
                    self.height
                )
                self.rects[i].set_pos_and_size(
                    self.rects[i].pos().x(),
                    self.rects[i].pos().y(),
                    point.x() - self.rects[i].pos().x(),
                    self.height
                )
                return i
        raise RuntimeError("UPWARDS FINISH WITHOUT RETURNING")

    def separator_position_changed(self, moved_separator: QGraphicsItem, point: QPointF) -> None:
        """
        Updates the rectangle positions and length according to the new position of moved_separator. This function
        should be called every time a Separator has moved.
        :param moved_separator: The separator that has moved.
        :param point: The position of the separator.
        """
        sep_index = self.find_separator(moved_separator)

        if sep_index is None:
            self.add_separator(moved_separator, point)
        else:
            if (point.y() < self.separators[sep_index][2].y() or
                    (point.y() == self.separators[sep_index][2].y() and
                     point.x() < self.separators[sep_index][2].x())):  # Separator moved upwards
                self.separators[sep_index][1] = self.update_upwards(self.separators[sep_index][1], point)

            elif (point.y() > self.separators[sep_index][2].y() or
                  (point.y() == self.separators[sep_index][2].y() and
                   point.x() > self.separators[sep_index][2].x())):  # Separator moved downwards
                self.separators[sep_index][1] = self.update_downwards(self.separators[sep_index][1], point)

            self.separators[sep_index][2] = point

    def separator_clicked_on_the_border(self, moved_separator: QGraphicsItem, cursor_point: QPointF,
                                        right_point: QPointF, left_point: QPointF) -> None:
        sep_index = self.find_separator(moved_separator)

        if sep_index is None:
            self.add_separator(moved_separator, right_point)
        else:
            # If the user released the separator in the right border and now the user is clicking in the left border
            # if self.separators[sep_index][2] == right_point and \
            #        (cursor_point - right_point).manhattanLength() > (cursor_point - left_point).manhattanLength():
            # Nothing is done because of the way function "update_downwards" is designed.

            # If the user released the separator in the left border and now the user is clicking in the right border
            if self.separators[sep_index][2] == left_point and \
                    (cursor_point - left_point).manhattanLength() > (cursor_point - right_point).manhattanLength():
                # Auxiliary variable to add clarity
                ind = self.separators[sep_index][1]

                self.rects[ind].set_pos_and_size(
                    self.rects[ind - 1].pos().x() + self.rects[ind - 1].rect().width(),
                    self.rects[ind - 1].pos().y(),
                    0,
                    self.height
                )

                self.separators[sep_index][1] -= 1

    def editable_text_changed_slot(self, editable_text_list: list[str]) -> None:
        """
        Change the background color of the rect depending on the text values of editable_text_list.
        :param editable_text_list: A list with the editable descriptor text parts.
        """
        index = 0
        editable_text_string = ""
        for i in range(len(editable_text_list)):
            editable_text_string += (str(i) + editable_text_list[i])
        try:
            index = list(self.colors.keys()).index(editable_text_string)
        except ValueError:
            pass
        """self.color_index = ind
        self.setBrush(QColor(list(self.colors.values())[ind]))
        self.update()"""

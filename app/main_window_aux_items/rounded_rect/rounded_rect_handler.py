import typing
from typing import List

from ..separator.separator import Separator

from PyQt5.QtCore import QPointF
from PyQt5.QtWidgets import (
    QGraphicsItem,
)
from .rounded_rect import RoundedRect


class RoundedRectHandler:
    """
    This class represents a multiple QGraphicsRectItem with rounded corners. It adjusts his text_size and
    the number of QGraphicsRectItem to fill the gap between the associated Separators.
    Assuming the "|" are the separators and the "=" are the rectangles, this is more or less what it will look like:
    |=====================================================================
    ======================================================================
    ====================================|
    """
    rects: list[RoundedRect]
    separators: list[list[Separator | int | QPointF]]
    points: list[tuple[float | int, tuple[float | int, float | int]]]
    colors: dict[str, str]
    color_indexes: list[int]

    def __init__(self, height: float | int, radius: float | int,
                 points: list[tuple[float | int, tuple[float | int, float | int]]], colors: dict[str, str],
                 parent: QGraphicsItem) -> None:
        """
        Create MultilineRoundedRect object.
        :param height: The height of the rectangles
        :param radius: The radius of the rounded corners
        :param points: The space between the border of a separator and
        :param colors: The colors
        :param parent: The QGraphicsItem parent of this Separator. Can't be None
        """
        self.height = height
        self.radius = radius
        self.parent = parent
        self.rects = []

        for line in points:
            self.rects.append(RoundedRect(line[1][0], line[0], line[1][1] - line[1][0], height, radius, parent))

        self.separators = []

        self.color_indexes = [0]
        self.colors = colors
        self.editable_text_changed_slot(-1, [])

    def add_separator_listeners(self, pos_changed_fn: typing.Any, clicked_on_the_border_fn: typing.Any,
                                removed_fn: typing.Any) -> None:
        pos_changed_fn.connect(self.separator_position_changed)
        clicked_on_the_border_fn.connect(self.separator_clicked_on_the_border)
        removed_fn.connect(self.separator_removed)

    def add_descriptor_listeners(self, editable_text_changed_fn: typing.Any) -> None:
        editable_text_changed_fn.connect(self.editable_text_changed_slot)

    def set_height_and_radius(self, height: float, radius: float) -> None:
        self.height = height
        self.radius = radius
        for rect in self.rects:
            rect.set_radius(radius)
            rect.set_pos_and_size(rect.pos().x(), rect.pos().y(), rect.rect().width(), self.height)

    def set_points_for_new_text(self, points: list[tuple[float, tuple[float, float]]], color: str) -> None:
        """
        Updates the points to place the rectangles when both separators have been moved at the same time, e.g. when
        resizing the window.
        """
        if len(points) > len(self.rects):  # We need to create more rects
            i = 0
            for i in range(len(self.rects)):
                self.rects[i].set_pos_and_size(
                    points[i][1][0],
                    points[i][0],
                    points[i][1][1] - points[i][1][0],
                    self.height
                )
                self.rects[i].set_background_color(color)
            for e in range(i + 1, len(points)):
                self.rects.append(RoundedRect(
                    points[e][1][0], points[e][0],
                    points[e][1][1] - points[e][1][0],
                    self.height,
                    self.radius,
                    self.parent)
                )
                self.rects[e].set_background_color(color)
        else:  # We need to delete part of existing rects
            i = 0
            for i in range(len(points)):
                self.rects[i].set_pos_and_size(
                    points[i][1][0],
                    points[i][0],
                    points[i][1][1] - points[i][1][0],
                    self.height
                )
                self.rects[i].set_background_color(color)
            for _ in range(i + 1, len(self.rects)):
                removed_rect = self.rects.pop()
                self.parent.scene().removeItem(removed_rect)

    def set_points(self, points: list[tuple[float, tuple[float, float]]], separator_points: list[QPointF],
                   new_text: bool) -> None:
        """
        Updates the points to place the rectangles when both separators have been moved at the same time, e.g. when
        resizing the window.
        """

        rects_colors_list = []
        if new_text:
            self.separators.clear()
            rects_colors_list.append(self.colors[""])
        else:
            if len(separator_points) != len(self.separators):
                raise RuntimeError("There are not the same points as separators in set_points() function")

            for sep in self.separators:
                rects_colors_list.append(self.rects[sep[1]].get_background_color())
            rects_colors_list.append(self.rects[-1].get_background_color())

        if len(separator_points) == 0:
            self.set_points_for_new_text(points, rects_colors_list[0])
        else:
            self.set_points_with_separators(points, separator_points, rects_colors_list)

    def set_points_with_separators(self, points: list[tuple[float, tuple[float, float]]],
                                   separator_points: list[QPointF], colors_list: list[str]) -> None:
        """
        Updates the points to place the rectangles when both separators have been moved at the same time, e.g. when
        resizing the window.
        """

        if len(separator_points) + len(points) > len(self.rects):  # We need to create more descriptors
            rect_index = 0
            sep_index = 0
            points_index = 0
            sep_find = False
            for rect_index in range(len(self.rects)):
                y_pos = points[points_index][0]
                if sep_find:
                    x_pos = separator_points[sep_index].x()
                    sep_find = False
                    sep_index += 1
                else:
                    x_pos = points[points_index][1][0]

                if sep_index < len(separator_points) and (
                        separator_points[sep_index].y() == points[points_index][0] and
                        separator_points[sep_index].x() <= points[points_index][1][1]):
                    width = separator_points[sep_index].x() - x_pos

                    # Update separators
                    self.separators[sep_index][1] = rect_index
                    self.separators[sep_index][2] = separator_points[sep_index]
                    sep_find = True
                else:
                    width = points[points_index][1][1] - x_pos
                    points_index += 1

                self.rects[rect_index].set_pos_and_size(x_pos, y_pos, width, self.height)
                self.rects[rect_index].set_background_color(colors_list[sep_index])

            for e in range(rect_index + 1, len(separator_points) + len(points)):
                y_pos = points[points_index][0]
                if sep_find:
                    x_pos = separator_points[sep_index].x()
                    sep_find = False
                    sep_index += 1
                else:
                    x_pos = points[points_index][1][0]

                if sep_index < len(separator_points) and (
                        separator_points[sep_index].y() == points[points_index][0] and
                        separator_points[sep_index].x() <= points[points_index][1][1]):
                    width = separator_points[sep_index].x() - x_pos

                    # Update separators
                    self.separators[sep_index][1] = rect_index
                    self.separators[sep_index][2] = separator_points[sep_index]
                    sep_find = True
                else:
                    width = points[points_index][1][1] - x_pos
                    points_index += 1

                self.rects.append(RoundedRect(x_pos, y_pos, width, self.height, self.radius, self.parent))
                self.rects[-1].set_background_color(colors_list[sep_index])

        else:  # We need to delete part of existing descriptors
            rect_index = 0
            sep_index = 0
            points_index = 0
            sep_find = False
            for rect_index in range(len(separator_points) + len(points)):
                y_pos = points[points_index][0]
                if sep_find:
                    x_pos = separator_points[sep_index].x()
                    sep_find = False
                    sep_index += 1
                else:
                    x_pos = points[points_index][1][0]

                if sep_index < len(separator_points) and (
                        separator_points[sep_index].y() == points[points_index][0] and
                        separator_points[sep_index].x() <= points[points_index][1][1]):
                    width = separator_points[sep_index].x() - x_pos

                    # Update separators
                    self.separators[sep_index][1] = rect_index
                    self.separators[sep_index][2] = separator_points[sep_index]
                    sep_find = True
                else:
                    width = points[points_index][1][1] - x_pos
                    points_index += 1

                self.rects[rect_index].set_pos_and_size(x_pos, y_pos, width, self.height)
                self.rects[rect_index].set_background_color(colors_list[sep_index])

            for _ in range(rect_index + 1, len(self.rects)):
                removed_rect = self.rects.pop()
                self.parent.scene().removeItem(removed_rect)

    def reset_colors(self):
        for i in range(len(self.color_indexes)):
            self.color_indexes[i] = 0

    def set_colors(self, colors: dict[str, str]) -> None:
        """
        Set the colors that will be used by the rounded rect depending on the value of the associated descriptor. The
        length of this dict should be the same as the possible combinations of the descriptor text plus one (the default
        one). Also, the colors list should be of any HTML valid color.
        :param colors: Dict of all available colors and the possibilities for the descriptor
        """
        self.colors = colors
        self.update_background_color_rects_group(-1, self.color_indexes[0])
        for i in range(len(self.separators)):
            self.update_background_color_rects_group(i, self.color_indexes[i + 1])

    def update_background_color_rects_group(self, separator_index: int, color_index):
        # Adapt bounds
        if separator_index == -1:
            start = 0
        else:
            start = self.separators[separator_index][1] + 1

        if separator_index == len(self.separators) - 1:
            end = len(self.rects)
        else:
            end = self.separators[separator_index + 1][1] + 1

        # Update background color for the rects of the same group
        for i in range(start, end):
            self.rects[i].set_background_color(list(self.colors.values())[color_index])

    def find_separator(self, separator: Separator) -> int:
        for i in range(len(self.separators)):
            if self.separators[i][0] is separator:
                return i

    def add_separator(self, separator: Separator, point: QPointF):
        if len(self.separators) == 0:
            self.separators.append([separator, self.insert_rect(point), point])

            # Add new color init_index entry for the new rects group
            self.color_indexes.append(0)
            self.update_background_color_rects_group(0, 0)
        else:
            for i in range(len(self.separators)):
                if (point.y() < self.separators[i][0].pos().y() or
                        (point.y() == self.separators[i][0].pos().y() and
                         point.x() < self.separators[i][0].pos().x())):
                    # [Separator, Last_index_before, Last_position]
                    self.separators.insert(i, [separator, self.insert_rect(point), point])

                    # Update "Last_index_before" for the separators after this separator
                    for e in range(i + 1, len(self.separators)):
                        self.separators[e][1] += 1

                    # Add new color init_index entry for the new rects group
                    self.color_indexes.insert(i + 1, 0)
                    self.update_background_color_rects_group(i, 0)
                    return

            # If the separator is inserted after the last separator
            self.separators.append([separator, self.insert_rect(point), point])

            # Add new color init_index entry for the new rects group
            self.color_indexes.append(0)
            self.update_background_color_rects_group(len(self.separators) - 1, 0)

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

        self.rects.append(RoundedRect(
            point.x(),
            point.y(),
            self.rects[-1].rect().width() + self.rects[-1].pos().x() - point.x(),
            self.height,
            self.radius,
            self.parent
        ))

        self.rects[-2].set_pos_and_size(
            self.rects[-2].pos().x(),
            self.rects[-2].pos().y(),
            point.x() - self.rects[-2].pos().x(),
            self.height
        )
        return len(self.rects) - 2

    def update_downwards(self, separator_index: int, init_index: int, point: QPointF) -> int:
        for i in range(init_index, len(self.rects)):
            if point.y() > self.rects[i].pos().y():
                self.rects[i].set_pos_and_size(
                    self.rects[i].pos().x(),
                    self.rects[i].pos().y(),
                    self.rects[i].rect().width() + self.rects[i + 1].rect().width(),
                    self.height
                )
                self.rects[i + 1].set_background_color(list(self.colors.values())[self.color_indexes[separator_index]])
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

    def update_upwards(self, separator_index: int, init_index: int, point: QPointF) -> int:
        for i in range(init_index, -1, -1):
            if point.y() < self.rects[i].pos().y():
                self.rects[i + 1].set_pos_and_size(
                    self.rects[i].pos().x(),
                    self.rects[i].pos().y(),
                    self.rects[i].rect().width() + self.rects[i + 1].rect().width(),
                    self.height
                )
                self.rects[i].set_background_color(list(self.colors.values())[self.color_indexes[separator_index + 1]])
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
                self.separators[sep_index][1] = self.update_upwards(sep_index, self.separators[sep_index][1], point)

            elif (point.y() > self.separators[sep_index][2].y() or
                  (point.y() == self.separators[sep_index][2].y() and
                   point.x() > self.separators[sep_index][2].x())):  # Separator moved downwards
                self.separators[sep_index][1] = self.update_downwards(sep_index, self.separators[sep_index][1], point)
            self.separators[sep_index][2] = point

    def separator_removed(self, separator: Separator):
        # Get indexes
        sep_index = self.find_separator(separator)
        rect_index = self.separators[sep_index][1]

        # Remove separator and descriptor
        removed_separator = self.separators.pop(sep_index)
        removed_rect = self.rects.pop(rect_index + 1)

        # Update "Last_index_before" for the separators after this separator
        for e in range(sep_index, len(self.separators)):
            self.separators[e][1] -= 1

        # Update remaining rects
        self.rects[rect_index].set_pos_and_size(
            self.rects[rect_index].pos().x(),
            self.rects[rect_index].pos().y(),
            self.rects[rect_index].rect().width() + removed_rect.rect().width(),
            self.height
        )

        self.color_indexes.pop(sep_index + 1)

        if sep_index == len(self.separators):
            end = len(self.rects)
        else:
            end = self.separators[sep_index][1] + 1

        # Update background color for the new group of rects
        for i in range(rect_index + 1, end):
            self.rects[i].set_background_color(list(self.colors.values())[self.color_indexes[sep_index]])

        self.parent.scene().removeItem(removed_rect)

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

                self.rects[ind].set_background_color(list(self.colors.values())[self.color_indexes[sep_index + 1]])

                self.separators[sep_index][1] -= 1

    def editable_text_changed_slot(self, separator_index: int, editable_text_list: list[str]) -> None:
        """
        Change the background color of the rounded_rect depending on the text values of editable_text_list.
        :param separator_index:
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

        self.color_indexes[separator_index + 1] = index
        self.update_background_color_rects_group(separator_index, index)

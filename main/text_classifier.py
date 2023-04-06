import numpy as np
from PyQt5.QtCore import QEvent, Qt, QPointF
from PyQt5.QtGui import QPen, QFont
from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsItem

import descriptor
from descriptor import Descriptor
from separator import Separator, find_nearest_point
from multiline_rounded_rect import MultilineRoundedRect


class TextClassifier(QGraphicsLineItem):
    """
    This class controls all the behaviour of the QGraphicsItems associated with the graphical text
    classification. That is, the rectangles and its descriptors and the separators between them.
    """
    descriptors: list[Descriptor]
    rects: list[MultilineRoundedRect]
    separators: list[Separator]

    def __init__(self, max_width: float, line_height: float, fixed_points: list[tuple[float, list[float]]],
                 default_text: str, colors: list[str], parent: QGraphicsItem) -> None:
        """
        Create TextClassifier object. Only one object form this class should be created
        :param max_width: The maximum width of this element. Is determined by the max text width.
        :param line_height: The height that the rectangles and the separators will have. Should be
                            greater than text height.
        :param fixed_points: Available points for the separators. The structure must
                             be [(y_0, [x_0, x_1, ...]), (y_1, [x_0, x_1, ...]), ...]
        :param default_text: The default text that will appear in the descriptors.
        :param colors: A list of colors that will be used by the rectangles as a background color depending on the
                       values of its Descriptors.
        :param parent: The QGraphicsItem parent of this element. Can't be None
        """
        super().__init__(parent)
        self.setOpacity(0)
        self.max_width = max_width
        self.height = line_height
        self.fixed_points = fixed_points
        self.default_text = default_text
        self.radius = line_height / 4
        self.offset = 0
        self.pen = None
        self.colors = self.set_color_list(colors)

        # Set separators
        self.separators = []
        self.separators.append(
            Separator(fixed_points[0][1][0], fixed_points[0][0], line_height, fixed_points, parent)
        )
        self.separators.append(
            Separator(fixed_points[-1][1][-1], fixed_points[-1][0], line_height, fixed_points, parent)
        )

        # Set immobile and not selectable the first and the last separator
        self.separators[0].setFlags(self.separators[0].flags() & ~QGraphicsItem.ItemIsMovable)
        self.separators[0].setCursor(Qt.ArrowCursor)
        self.separators[1].setFlags(self.separators[1].flags() & ~QGraphicsItem.ItemIsMovable)
        self.separators[1].setCursor(Qt.ArrowCursor)

        # Set filters
        self.separators[0].installSceneEventFilter(self)
        self.separators[1].installSceneEventFilter(self)

        # Set rectangles
        self.rects = []
        self.rects.append(MultilineRoundedRect(max_width, line_height, self.radius, self.offset, self.colors, parent))
        self.rects[0].init_separators((self.separators[0], self.separators[1]))

        # Set descriptors
        self.descriptors = []
        self.descriptors.append(Descriptor(max_width, line_height * 1.2, default_text, line_height / 3, parent))
        self.descriptors[0].init_separators((self.separators[0], self.separators[1]))
        self.descriptors[0].editable_text_changed.connect(self.rects[0].editable_text_changed_slot)

    def reset(self, fixed_points: list[tuple[float, list[float]]]) -> None:
        """
        Reset the object with new fixed points. That is, remove all the separators except the first ant the last and
        all the associated multiline rounded rects and descriptors.
        :param fixed_points: The new fixed_points
        """
        self.fixed_points = fixed_points

        self.rects[0].init_separators((self.separators[0], self.separators[-1]))
        self.descriptors[0].init_separators((self.separators[0], self.separators[-1]))

        last_index = len(self.separators) - 1

        for _ in range(1, last_index):
            removed_rect = self.rects.pop(1)
            removed_descriptor = self.descriptors.pop(1)
            removed_separator = self.separators.pop(1)

            self.scene().removeItem(removed_rect)
            self.scene().removeItem(removed_descriptor)
            self.scene().removeItem(removed_separator)

        self.separators[0].fixed_points = fixed_points
        self.separators[1].fixed_points = fixed_points

        self.separators[0].setPos(fixed_points[0][1][0], fixed_points[0][0])
        self.separators[1].setPos(fixed_points[-1][1][-1], fixed_points[-1][0])

        self.rects[0].update_points(self.separators[0])
        self.rects[0].update()
        self.descriptors[0].update_points(self.separators[0])
        self.descriptors[0].update()

    def set_color_list(self, color_list: list[str]) -> dict[str, list[str]]:
        """
        Create a dictionary from a list of colors. This dictionary will have as a key of each element the color
        itself and as a value, a list containing the values of the different editable parts of the descriptor text.
        :param color_list: The list with the colors.
        :return: The dictionary.
        """
        editable_texts_number = len(self.default_text.split(descriptor.TEXT_SEPARATOR)) - 1
        allo_str_len = len(descriptor.ALLOWED_STRINGS)

        if len(color_list) != np.power(allo_str_len, editable_texts_number) + 1:
            raise RuntimeError("There should be " + str(np.power(allo_str_len, editable_texts_number) + 1) +
                               " colors for text_classifier module but got " + str(len(color_list)) + " instead.")

        colors = {color_list[0]: []}

        for i in range(1, len(color_list) - 1):
            value = []
            for e in reversed(range(editable_texts_number)):
                if e == 0:
                    value.append(descriptor.ALLOWED_STRINGS[i % allo_str_len])
                else:
                    value.append(descriptor.ALLOWED_STRINGS[np.floor_divide(i, allo_str_len * e) % allo_str_len])
            colors[color_list[i]] = value
        return colors

    def set_default_descriptor(self, default_descriptor: str, colors: list[str]) -> None:
        """
        Set the default descriptor for all the descriptors. Should contain one or more "~" characters. The list of
        colors will be the colors that the rounded rects will have depending on the value of the descriptor. The length
        of this list should be the same as the possible combinations of the descriptor text plus one (the default one).
        Also, the colors list should be of any HTML valid color.
        :param default_descriptor: The default string that will appear in the descriptor. Should contain one or more
                                   "~" characters.
        :param colors: List of all available colors
        """
        self.default_text = default_descriptor
        self.colors = self.set_color_list(colors)
        for rect in self.rects:
            rect.colors = self.colors

        for desc in self.descriptors:
            desc.set_default_text(default_descriptor)

    def set_separator_pen(self, pen: QPen) -> None:
        """
        Apply the given pen to all the separators
        :param pen: the pen to be applied
        """
        self.pen = pen
        for separator in self.separators:
            separator.setPen(pen)

    def set_multiline_rects_offset(self, offset: int | float) -> None:
        """
        Set the offset for all the multiline rounded rects
        :param offset: The offset in pixels
        """
        for rect in self.rects:
            rect.offset = offset

    def set_descriptors_font(self, font: QFont) -> None:
        """
        Set a font for all the descriptors.
        :param font: The requested font
        """
        for item in self.descriptors:
            item.setFont(font)

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

    def get_separator_points(self) -> list[QPointF]:
        """
        Return a list with the coordinates of all separators.
        :return: The list of coordinates
        """
        return [sep.pos() for sep in self.separators]

    def set_separator_points(self, points: list[QPointF]) -> None:
        """
        Set the coordinates of all separators with the given QPointF list.
        :param points: The points list.
        """
        if len(points) != len(self.separators):
            raise RuntimeError("There are not the same points as separators in set_separator_points() function")

        for i in range(len(points)):
            self.separators[i].setPos(points[i])

    def update_general_fixed_points_and_separators_pos(self, new_fixed_points: list[tuple[float, list[float]]],
                                                       new_separator_points: list[QPointF]) -> None:
        """
        Update the fixed points and the position of all the separators. This function should be called if the
        text size or the text itself changes.
        :param new_fixed_points: The new fixed points for yhe text_classifier object.
        :param new_separator_points: The new location for all the separators.
        """
        self.fixed_points = new_fixed_points

        # To update the specifics fixed_points for the separators, first we change its fixed_points to the generic
        # fixed_points, then we specify the position for all the separators and finally, we change the fixed_points
        # to restrict the separator movement

        for separator in self.separators:
            separator.fixed_points = new_fixed_points

        self.set_separator_points(new_separator_points)

        for i in range(len(self.separators)):
            self.update_fixed_points_separator(i)

        # Update all the rects and the descriptors to adjust to new separator positions
        for i in range(len(self.rects)):
            self.rects[i].update_points(self.separators[i])
            self.rects[i].update()
            self.descriptors[i].update_points(self.separators[i])
            self.descriptors[i].update()

    def set_line_height(self, line_height: float | int) -> None:
        """
        Set line height for all the separators, rects and descriptors. In the case of the descriptors, the value
        modified will be the y_offset, to adjust to the new rect height. In the case of the rects, the radius will
        also be modified.
        :param line_height: Line height in pixels.
        """
        self.height = line_height
        self.radius = line_height / 4

        for rect in self.rects:
            rect.radius = self.radius
            rect.setRect(0, 0, 1, self.height)

        for separator in self.separators:
            separator.set_height(self.height)

        for descript in self.descriptors:
            descript.y_offset = self.height * 1.2
            descript.set_text_size(self.height / 3)

    def set_width(self, width: float | int) -> None:
        """
        Set width for all the rects and descriptors.
        :param width: Width in pixels
        """
        self.max_width = width

        for rect in self.rects:
            rect.set_max_width(width)

        for descript in self.descriptors:
            descript.set_max_width(width)

    def point_is_occupied(self, x: float, y: float) -> tuple[bool, int]:
        """
        Check if the given point is occupied by existing separator and return the index of separator.
        :param x: The x coordinate
        :param y: The y coordinate
        :return: A tuple. The first element is True if the point is occupied, False if not. The second element is the
        index of the separator if the position is occupied. If the position is not occupied, this second element will
        be the index of the separator before. A -1 will show an error.
        """
        # Find nearest available point
        real_y = find_nearest_point(self.get_y_values(), y)
        real_x = find_nearest_point(self.get_x_values(real_y), x)

        for i in range(len(self.separators)):
            if self.separators[i].is_on_the_border():
                if ((self.separators[i].complete_pos(True).x() == real_x and
                     self.separators[i].complete_pos(True).y() == real_y) or
                        (self.separators[i].complete_pos(False).x() == real_x and
                         self.separators[i].complete_pos(False).y() == real_y)):
                    return True, i
            else:
                if self.separators[i].complete_pos(True).x() == real_x and self.separators[i].complete_pos(
                        True).y() == real_y:
                    return True, i
            if self.separators[i].complete_pos(False).y() > real_y or \
                    (self.separators[i].complete_pos(False).y() == real_y and self.separators[i].complete_pos(
                        False).x() > real_x):
                return False, i - 1
        return True, -1

    def find_free_point(self, x: float, y: float) -> tuple[float, float, int]:
        """
        Check if the given point is occupied by existing separator and if so, find another free point.
        The search goes from left to right and from up to down.
        :param x: The x coordinate
        :param y: The y coordinate
        :return: The same point if is free or new point if it is busy. If there are no points available,
                 this function will return (-1000,-1000)
        """
        # This auxiliary variable will reduce the search because all the separators with lower
        # indexes won't affect availability check
        is_occupied, index = self.point_is_occupied(x, y)
        if not is_occupied:
            real_y = find_nearest_point(self.get_y_values(), y)
            real_x = find_nearest_point(self.get_x_values(real_y), x)
            return real_x, real_y, index
        elif index != -1:
            real_y = find_nearest_point(self.get_y_values(), y)
            real_x = find_nearest_point(self.get_x_values(real_y), x)

            for line in self.fixed_points:
                if line[0] >= real_y:
                    for i in range(len(line[1])):
                        if (line[0] == real_y and line[1][i] >= real_x) or line[0] > real_y:
                            if self.separators[index].is_on_the_border():
                                if not (i == 0 or i == len(line[1]) - 1):
                                    return line[1][i], line[0], index - 1
                                if i == 0:
                                    # If this position is busy, increment by one the index in separators array
                                    index += 1
                            elif self.separators[index].complete_pos(True).x() == line[1][i] and \
                                    self.separators[index].complete_pos(True).y() == line[0]:
                                # If this position is busy, increment by one the index in separators array
                                index += 1
                            else:
                                return line[1][i], line[0], index - 1
        return -1000, -1000, -1

    def split(self, x: float, y: float) -> bool:
        """
        Splits the nearest rectangle to the given coordinates in two, placing a separator where
        the split has been made.
        :param x: The x coordinate
        :param y: The y coordinate
        :return: True if success, False if error. There can be a mistake if the coordinates
                 are out of bounds or if there is no more space to place a separator
        """
        real_x, real_y, index = self.find_free_point(x, y)

        if (real_x == -1000 and real_y == -1000) or index == -1:
            return False

        # Create needed new elements
        new_separator = Separator(
            real_x,
            real_y,
            self.height,
            self.set_fixed_points_for_new_separator(index),
            self.parentItem()

        )
        new_rect = MultilineRoundedRect(
            self.max_width,
            self.height,
            self.radius,
            self.offset,
            self.colors,
            self.parentItem()
        )
        new_descriptor = Descriptor(
            self.max_width, self.height * 1.2, self.default_text, self.height / 3, self.parentItem()
        )
        new_separator.installSceneEventFilter(self)
        new_separator.setPen(self.pen)

        new_descriptor.editable_text_changed.connect(new_rect.editable_text_changed_slot)

        self.separators.insert(index + 1, new_separator)
        self.rects.insert(index + 1, new_rect)
        self.rects[index].init_separators((self.separators[index], self.separators[index + 1]))
        self.rects[index + 1].init_separators((self.separators[index + 1], self.separators[index + 2]))

        self.descriptors.insert(index + 1, new_descriptor)
        self.descriptors[index].init_separators((self.separators[index], self.separators[index + 1]))
        self.descriptors[index + 1].init_separators((self.separators[index + 1], self.separators[index + 2]))

        self.update_fixed_points_separator(index)
        self.update_fixed_points_separator(index + 2)

        return True

    def join(self, x: float, y: float) -> bool:
        """
        Remove a separator and join the two remaining rectangles.
        :param x: The x coordinate
        :param y: The y coordinate
        :return: True if success, False if error. There can be a mistake if the coordinates
                 are out of bounds or if in the given coordinates there is no separator
        """
        is_occupied, index = self.point_is_occupied(x, y)
        if not is_occupied:
            return False

        removed_rect = self.rects.pop(index)
        removed_descriptor = self.descriptors.pop(index)
        removed_separator = self.separators.pop(index)

        self.update_fixed_points_separator(index - 1)
        self.update_fixed_points_separator(index)

        self.rects[index - 1].init_separators((self.separators[index - 1], self.separators[index]))
        self.descriptors[index - 1].init_separators((self.separators[index - 1], self.separators[index]))

        self.scene().removeItem(removed_rect)
        self.scene().removeItem(removed_descriptor)
        self.scene().removeItem(removed_separator)

        return True

    def set_fixed_points_for_new_separator(self, index: int) -> list[tuple[float, list[float]]]:
        """
        Set the fixed points for the new created separator
        :param index: Index of the element after which the new separator is to be inserted
        :return: The fixed_points structure for the new separator
        """
        start_x = self.separators[index].complete_pos(True).x()
        start_y = self.separators[index].complete_pos(True).y()

        end_x = self.separators[index + 1].complete_pos(False).x()
        end_y = self.separators[index + 1].complete_pos(False).y()
        return self.set_fixed_points(start_x, start_y, end_x, end_y)

    def set_fixed_points(self,
                         start_x: float, start_y: float,
                         end_x: float, end_y: float
                         ) -> list[tuple[float, list[float]]]:
        """
        Obtain, from self.fixed_points the subgroup of points that are between start point and end point.
        The format of structure returned is the same as self.fixed_points.
        :param start_x: The x coordinate of the starting point
        :param start_y: The y coordinate of the starting point
        :param end_x: The x coordinate of the ending point
        :param end_y: The y coordinate of the ending point
        :return: The new fixed_points structure
        """
        new_fixed_points = []
        for line in self.fixed_points:
            if end_y >= line[0]:
                if line[0] >= start_y:
                    start_recording = True
                    for x_value in line[1]:
                        if ((line[0] == start_y and x_value > start_x) or line[0] > start_y) and \
                                ((line[0] == end_y and x_value < end_x) or line[0] < end_y):
                            if start_recording:
                                start_recording = False
                                new_fixed_points.append((line[0], []))
                            new_fixed_points[-1][1].append(x_value)
            else:
                break  # If left values are higher, end loop

        return new_fixed_points

    def update_fixed_points_separator(self, index: int) -> None:
        """
        Update the fixed_points of the separator for a given index separator.
        :param index: Index of the separator
        """
        if (len(self.separators) - 2) >= index >= 1:
            self.separators[index].fixed_points = self.set_fixed_points(
                self.separators[index - 1].complete_pos(True).x(),
                self.separators[index - 1].complete_pos(True).y(),
                self.separators[index + 1].complete_pos(False).x(),
                self.separators[index + 1].complete_pos(False).y()
            )

    def sceneEventFilter(self, watched: QGraphicsItem, event: QEvent) -> bool:
        """
        Filters events for the item watched. event is the filtered event.

        In this case, this function only watch Separator items, and it is used to update the fixed_points
        of the surrounding separators.

        :param watched: Item from which the event has occurred
        :param event: The object that indicates the type of event triggered
        :return: False, to allow the event to be treated by other Items
        """
        if isinstance(event, QEvent) and event.type() == QEvent.UngrabMouse:
            if isinstance(watched, Separator):
                self.update_fixed_points_separator(self.separators.index(watched) - 1)
                self.update_fixed_points_separator(self.separators.index(watched) + 1)
        return False

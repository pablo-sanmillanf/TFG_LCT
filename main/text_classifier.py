import numpy as np
from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtGui import QPen
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
        :param parent: The QGraphicsItem parent of this element. Can't be None
        """
        super().__init__(0, 0, 0, 1, parent)
        self.setOpacity(0)
        self.max_width = max_width
        self.height = line_height
        self.fixed_points = fixed_points
        self.default_text = default_text
        self.radius = 5
        self.offset = 2
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
        self.descriptors.append(Descriptor(max_width, default_text, parent))
        self.descriptors[0].init_separators((self.separators[0], self.separators[1]))
        self.descriptors[0].editable_text_changed.connect(self.rects[0].editable_text_changed_slot)

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
                               "colors for text_classifier module but got" + str(len(color_list)) + "instead.")

        colors = {color_list[0]: []}

        for i in range(1, len(color_list) - 1):
            value = []
            for e in reversed(range(editable_texts_number)):
                if e == 0:
                    value.append(descriptor.ALLOWED_STRINGS[i % allo_str_len])
                else:
                    value.append(descriptor.ALLOWED_STRINGS[np.floor_divide(i, allo_str_len*e) % allo_str_len])
            colors[color_list[i]] = value
        return colors

    def set_separator_pen(self, pen: QPen) -> None:
        """
        Apply the given pen to all the separators
        :param pen: the pen to be applied
        """
        self.pen = pen
        for separator in self.separators:
            separator.setPen(pen)

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

    def get_separator_points(self) -> list[tuple[float, float]]:
        """
        Return a list with the coordinates of all separators.
        :return: The list of coordinates
        """
        return [(sep.pos().x(), sep.pos().y()) for sep in self.separators]

    def check_point_availability(self, x: float, y: float) -> tuple[float, float]:
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
        separator_index = self.find_index_separator(x, y)
        if separator_index != -1:
            for line in self.fixed_points:
                if line[0] >= y:
                    for i in range(len(line[1])):
                        if (line[0] == y and line[1][i] >= x) or line[0] > y:
                            if self.separators[separator_index].is_on_the_border():
                                if not (i == 0 and i == len(line[1]) - 1):
                                    return line[1][i], line[0]
                                if i == 0:
                                    # If this position is busy, increment by one the index in separators array
                                    separator_index += 1
                            elif self.separators[separator_index].complete_pos(True).x() == line[1][i] and \
                                    self.separators[separator_index].complete_pos(True).y() == line[0]:
                                # If this position is busy, increment by one the index in separators array
                                separator_index += 1
                            else:
                                return line[1][i], line[0]
        return -1000, -1000

    def find_index_separator(self, x: float, y: float) -> int:
        """
        Finds, among the existing separators, the separator before the given coordinates
        :param x: The x coordinate
        :param y: The y coordinate
        :return: The index of the separator before or -1 if error
        """
        for i in range(len(self.separators)):
            # Check if this separator is in subsequent lines
            if self.separators[i].complete_pos(True).y() > y:
                return i - 1
            elif self.separators[i].complete_pos(True).y() == y and self.separators[i].complete_pos(True).x() > x:
                return i - 1
            if self.separators[i].is_on_the_border():
                if self.separators[i].complete_pos(False).y() > y:
                    return i - 1
                elif self.separators[i].complete_pos(False).y() == y and self.separators[i].complete_pos(False).x() > x:
                    return i - 1
        return -1

    def split(self, x: float, y: float) -> bool:
        """
        Splits the nearest rectangle to the given coordinates in two, placing a separator where
        the split has been made.
        :param x: The x coordinate
        :param y: The y coordinate
        :return: True if success, False if error. There can be a mistake if the coordinates
                 are out of bounds or if there is no more space to place a separator
        """
        # Find nearest available point
        real_y = find_nearest_point(self.get_y_values(), y)
        real_x = find_nearest_point(self.get_x_values(real_y), x)

        real_x, real_y = self.check_point_availability(real_x, real_y)

        if real_x == -1000 and real_y == -1000:
            return False

        index = self.find_index_separator(real_x, real_y)
        if index == -1:
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
        new_descriptor = Descriptor(self.max_width, self.default_text, self.parentItem())
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
        # Find nearest available point
        real_y = find_nearest_point(self.get_y_values(), y)
        real_x = find_nearest_point(self.get_x_values(real_y), x)

        index = self.find_index_separator(real_x, real_y)
        if index == -1:
            return False

        if self.separators[index].complete_pos(True).x() != real_x or \
                self.separators[index].complete_pos(True).y() != real_y:
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

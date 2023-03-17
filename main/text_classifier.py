from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsItem

from separator import Separator, find_nearest_point
from resizable_rect import MultilineRoundedRect


class TextClassifier(QGraphicsLineItem):
    rects: list[MultilineRoundedRect]
    separators: list[Separator]

    def __init__(self, size, fixed_points, parent):
        super().__init__(0, 0, 0, 1, parent)
        self.setOpacity(0)
        self.size = size
        self.fixed_points = fixed_points
        self.parent = parent
        self.radius = 5
        self.offset = 2
        self.pen = None

        self.separators = []
        self.separators.append(Separator(fixed_points[0][1][0], fixed_points[0][0], size, parent, fixed_points))
        self.separators.append(Separator(fixed_points[-1][1][-1], fixed_points[-1][0], size, parent, fixed_points))

        # Set immobile the first and the last separator
        self.separators[0].setFlags(self.separators[0].flags() & ~QGraphicsItem.ItemIsMovable)
        self.separators[1].setFlags(self.separators[1].flags() & ~QGraphicsItem.ItemIsMovable)

        # Set filters
        self.separators[0].installSceneEventFilter(self)
        self.separators[1].installSceneEventFilter(self)
        self.rects = []
        self.rects.append(MultilineRoundedRect(size, self.radius, self.offset, parent))
        self.rects[0].init_separators((self.separators[0], self.separators[1]))

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
                    for x_value in line[1]:
                        if (line[0] == y and x_value >= x) or line[0] > y:
                            if self.separators[separator_index].pos().x() == x_value and \
                                    self.separators[separator_index].pos().y() == line[0]:
                                # If this position is busy, increment by one the index in separators array
                                separator_index += 1
                            else:
                                return x_value, line[0]
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
            if self.separators[i].pos().y() > y:
                return i - 1
            elif self.separators[i].pos().y() == y and self.separators[i].pos().x() > x:
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
            self.size,
            self.parent,
            self.set_fixed_points_for_new_separator(index)
        )
        new_rect = MultilineRoundedRect(self.size, self.radius, self.offset, self.parent)
        new_separator.installSceneEventFilter(self)
        new_separator.setPen(self.pen)

        self.separators.insert(index + 1, new_separator)
        self.rects.insert(index + 1, new_rect)
        self.rects[index].init_separators((self.separators[index], self.separators[index + 1]))
        self.rects[index + 1].init_separators((self.separators[index + 1], self.separators[index + 2]))

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

        if self.separators[index].pos().x() != real_x or self.separators[index].pos().y() != real_y:
            return False

        removed_separator = self.separators.pop(index)
        removed_rect = self.rects.pop(index)
        self.scene().removeItem(removed_separator)
        self.scene().removeItem(removed_rect)

        self.rects[index - 1].init_separators((self.separators[index - 1], self.separators[index]))

        return True

    def set_fixed_points_for_new_separator(self, index: int) -> list[tuple[float, list[float]]]:
        """
        Set the fixed points for the new created separator
        :param index: Index of the element after which the new separator is to be inserted
        :return: The fixed_points structure for the new separator
        """
        start_x = self.separators[index].pos().x()
        start_y = self.separators[index].pos().y()

        end_x = self.separators[index + 1].pos().x()
        end_y = self.separators[index + 1].pos().y()
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

    def sceneEventFilter(self, watched, event):
        if isinstance(event, QEvent) and event.type() == QEvent.UngrabMouse:
            if isinstance(watched, Separator):
                index = self.separators.index(watched)
                if index != 0 and index != (len(self.separators) - 1):
                    # Set fixed points for the anterior and posterior Separator
                    if index != 1:
                        self.separators[index - 1].fixed_points = self.set_fixed_points(
                            self.separators[index - 2].pos().x(),
                            self.separators[index - 2].pos().y(),
                            self.separators[index].pos().x(),
                            self.separators[index].pos().y()
                        )
                    if index != (len(self.separators) - 2):
                        self.separators[index + 1].fixed_points = self.set_fixed_points(
                            self.separators[index].pos().x(),
                            self.separators[index].pos().y(),
                            self.separators[index + 2].pos().x(),
                            self.separators[index + 2].pos().y()
                        )

        return False

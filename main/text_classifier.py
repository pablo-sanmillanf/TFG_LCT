from PyQt5.QtGui import QPen

from separator import Separator, find_nearest_point
from resizable_rect import MultilineRoundedRect


class TextClassifier:
    rects: list[MultilineRoundedRect]
    separators: list[Separator]

    def __init__(self, size, fixed_points, parent):
        self.size = size
        self.fixed_points = fixed_points
        self.parent = parent
        self.radius = 5
        self.offset = 2
        self.pen = None

        self.separators = []
        self.separators.append(Separator(fixed_points[0][1][0], fixed_points[0][0], size, parent, fixed_points))
        self.separators.append(Separator(fixed_points[-1][1][-1], fixed_points[-1][0], size, parent, fixed_points))
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

        # Create needed new elements
        new_separator = Separator(real_x, real_y, self.size, self.parent, self.fixed_points)
        new_rect = MultilineRoundedRect(self.size, self.radius, self.offset, self.parent)

        new_separator.setPen(self.pen)

        index = self.find_index_separator(real_x, real_y)
        if index == -1:
            return False

        self.separators.insert(index + 1, new_separator)
        self.rects.insert(index + 1, new_rect)
        self.rects[index].init_separators((self.separators[index], self.separators[index + 1]))
        self.rects[index + 1].init_separators((self.separators[index + 1], self.separators[index + 2]))

        return True



from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import QGraphicsItem

from .separator import Separator, find_nearest_point, SeparatorEmitter


class SeparatorHandler:
    """
    This class controls all the behaviour of the Separators (insertion, deletion, updates, movement, etc.).
    """
    separators: list[Separator]

    def __init__(self, line_height: float, fixed_points: list[tuple[float, list[float]]],
                 parent: QGraphicsItem) -> None:
        """
        Create SeparatorHandler object. Only one object from this class should be created
        :param line_height: The height that the separators will have.
        :param fixed_points: Available points for the separators. The structure must
                             be [(y_0, [x_0, x_1, ...]), (y_1, [x_0, x_1, ...]), ...]
        :param parent: The QGraphicsItem parent of the Separators. Can't be None
        """
        self.height = line_height
        self.fixed_points = fixed_points
        self.parent = parent
        self.pen = None
        self.emitter = SeparatorEmitter()

        # Set separators
        self.separators = []

        self.emitter.released.connect(self.separator_is_released)

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

    def get_separator_points(self) -> list[QPointF]:
        """
        Return a list with the coordinates of all separators.
        :return: The list of coordinates
        """
        return [sep.pos() for sep in self.separators]

    def point_is_occupied(self, x: float, y: float) -> tuple[bool, int]:
        """
        Check if the given point is occupied by existing separator and return the ind of separator. Should be called
        when no Separator is moved. Should be called when exist at least one Separator.
        :param x: The x coordinate
        :param y: The y coordinate
        :return: A tuple. The first element is True if the point is occupied, False if not. The second element is the
        ind of the separator if the position is occupied. If the position is not occupied, this second element will
        be the ind of the separator before. A -1 will show an error.
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
            if self.separators[i].complete_pos(True).y() > real_y or \
                    (self.separators[i].complete_pos(True).y() == real_y and self.separators[i].complete_pos(
                        True).x() > real_x):
                return False, i - 1
        return True, -1

    def find_free_point(self, x: float, y: float) -> tuple[float, float, int]:
        """
        Check if the given point is occupied by existing separator and if so, find another free point.
        The search goes from left to right and from up to down.
        :param x: The x coordinate
        :param y: The y coordinate
        :return: The same point if is free or new point if it is busy and the ind of the previous separator. If there
                 are no points available, this function will return (None, None, -1)
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
                                    # If this position is busy, increment by one the ind in separators array
                                    index += 1
                            elif self.separators[index].complete_pos(True).x() == line[1][i] and \
                                    self.separators[index].complete_pos(True).y() == line[0]:
                                # If this position is busy, increment by one the ind in separators array
                                index += 1
                            else:
                                return line[1][i], line[0], index - 1
        return None, None, -1

    def add_separator(self, x: float, y: float, is_static: bool) -> bool:
        """
        Add a separator in the nearest valid position. The two first added separators should be the bottom and upper
        limits for all the rest of the separator.
        :param x: The x coordinate
        :param y: The y coordinate
        :param is_static: True if the separator won't move, False otherwise.
        :return: The created separator if success, None if error. There can be an error if the coordinates
                 are out of bounds or if there is no more space to place a separator
        """
        if len(self.separators) <= 1:
            real_y = find_nearest_point(self.get_y_values(), y)
            real_x = find_nearest_point(self.get_x_values(real_y), x)
            index = len(self.separators) - 1
            # Create needed new elements
            new_separator = Separator(
                real_x,
                real_y,
                self.height,
                self.fixed_points,
                self.emitter,
                self.parent

            )
        else:
            real_x, real_y, index = self.find_free_point(x, y)

            if (real_x is None and real_y is None) or index == -1:
                return False

            # Create needed new elements
            new_separator = Separator(
                real_x,
                real_y,
                self.height,
                self.set_fixed_points_for_new_separator(index),
                self.emitter,
                self.parent

            )
        if is_static:
            new_separator.setFlags(new_separator.flags() & ~QGraphicsItem.ItemIsMovable)
            new_separator.setCursor(Qt.ArrowCursor)

        if self.pen is not None:
            new_separator.setPen(self.pen)

        self.separators.insert(index + 1, new_separator)

        self.update_fixed_points_separator(index)
        self.update_fixed_points_separator(index + 2)

        return True

    def delete_separator(self, x: float, y: float) -> Separator | None:
        """
        Remove a separator.
        :param x: The x coordinate
        :param y: The y coordinate
        :return: The created separator if success, None if error. There can be an error if the coordinates
                 are out of bounds or if in the given coordinates there is no separator
        """
        is_occupied, index = self.point_is_occupied(x, y)
        if not is_occupied:
            return None

        removed_separator = self.separators.pop(index)

        self.update_fixed_points_separator(index - 1)
        self.update_fixed_points_separator(index)

        self.parent.scene().removeItem(removed_separator)

        self.emitter.removed.emit(removed_separator)

        return removed_separator

    def delete_all_separators(self) -> None:
        """
        Remove all the separators.
        """
        for _ in range(len(self.separators)):
            removed_separator = self.separators.pop()
            self.parent.scene().removeItem(removed_separator)

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
        Update the fixed_points of the separator for a given ind separator.
        :param index: Index of the separator
        """
        if (len(self.separators) - 2) >= index >= 1:
            self.separators[index].fixed_points = self.set_fixed_points(
                self.separators[index - 1].complete_pos(True).x(),
                self.separators[index - 1].complete_pos(True).y(),
                self.separators[index + 1].complete_pos(False).x(),
                self.separators[index + 1].complete_pos(False).y()
            )

    def separator_is_released(self, separator: Separator) -> None:
        """
        Updates the fixed-points of the surrounding separators.
        :param separator: The separator that has been released.
        """
        self.update_fixed_points_separator(self.separators.index(separator) - 1)
        self.update_fixed_points_separator(self.separators.index(separator) + 1)

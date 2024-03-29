from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPen, QColor
from PyQt5.QtWidgets import QGraphicsItem

from .separator import Separator, find_nearest_point, SeparatorEmitter

SUPER_SEPARATOR_FACTOR = 1.5


class SeparatorHandler:
    """
    This class controls all the behaviour of the Separators (insertion, deletion, updates, movement, etc.). Also,
    manges the creation and elimination of the super Separators.
    """
    _regular_pen: QPen
    _super_pen: QPen
    separators: list[list[Separator | bool]]  # Element: [Separator_object, Is_super_separator]

    def __init__(self, line_height: float, fixed_points: list[tuple[float, list[tuple[float, bool]]]],
                 regular_sep_color: str, super_sep_color: str, parent: QGraphicsItem) -> None:
        """
        Create SeparatorHandler object. Only one object from this class should be created
        :param line_height: The height that the separators will have.
        :param fixed_points: Available points for the separators. The structure must be
                            [
                            (y_0, [(x_0, Ignored), (x_1, Ignored), ...]),
                            (y_1, [(x_0, Ignored), (x_1, Ignored), ...]),
                            ...
                            ]
        :param regular_sep_color: A valid HTML color that will have the regular separators.
        :param super_sep_color: A valid HTML color that will have the super separators.
        :param parent: The QGraphicsItem parent of the Separators. Can't be None
        """
        self._height = line_height
        self._fixed_points = fixed_points
        self._parent = parent
        self.emitter = SeparatorEmitter()

        self._regular_pen = Separator(
            self._fixed_points[0][1][0][0],
            self._fixed_points[0][0],
            self._height,
            self._fixed_points,
            None,
            self._parent
        ).pen()
        self._super_pen = QPen(self._regular_pen)
        self._regular_pen.setColor(QColor(regular_sep_color))
        self._super_pen.setColor(QColor(super_sep_color))
        self._super_pen.setWidthF(self._super_pen.widthF() * SUPER_SEPARATOR_FACTOR)

        # Set separators
        self.separators = []

        self.emitter.released.connect(self._separator_is_released)

    def set_fixed_points(self, fixed_points: list[tuple[float, list[tuple[float, bool]]]]) -> None:
        """
        Sets the point structure through which the Separators can be moved.
        """
        self._fixed_points = fixed_points

    def set_separator_colors(self, regular_sep_color: str, super_sep_color: str) -> None:
        """
        Apply the colors to all the separators
        :param regular_sep_color: A valid HTML color that will have the regular separators.
        :param super_sep_color: A valid HTML color that will have the super separators.
        """
        self._regular_pen.setColor(QColor(regular_sep_color))
        self._super_pen.setColor(QColor(super_sep_color))

        for separator in self.separators:
            if separator[1]:
                separator[0].setPen(self._super_pen)
            else:
                separator[0].setPen(self._regular_pen)

    def set_separator_width(self, width: float) -> None:
        """
        Set the width to all the Separators. If there is a super Separator, the width is multiplied by
        SUPER_SEPARATOR_FACTOR.
        :param width: the width
        """
        self._regular_pen.setWidthF(width)
        self._super_pen.setWidthF(width * SUPER_SEPARATOR_FACTOR)
        for separator in self.separators:
            if separator[1]:
                separator[0].setPen(self._super_pen)
            else:
                separator[0].setPen(self._regular_pen)

    def set_separator_height(self, height: float) -> None:
        """
        Set the height to all the Separators.
        :param height: the height
        """
        self._height = height
        for separator in self.separators:
            separator[0].set_height(height)

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

    def get_separator_points(self) -> list[QPointF]:
        """
        Return a list with the coordinates of all separators.
        :return: The list of coordinates
        """
        return [self.separators[i][0].pos() for i in range(1, len(self.separators) - 1)]

    def get_super_separator_points(self) -> list[QPointF]:
        """
        Return a list with the coordinates of all the super separators.
        :return: The list of coordinates
        """
        return [self.separators[i][0].pos() for i in range(1, len(self.separators) - 1) if self.separators[i][1]]

    def set_separator_points(self, points: list[QPointF]) -> None:
        """
        Set the coordinates of all separators with the given QPointF list.
        :param points: The points list.
        """
        if len(points) != len(self.separators):
            raise RuntimeError("There are not the same points as separators in set_separator_points() function")

        for i in range(len(points)):
            self.separators[i][0].set_fixed_points(self._fixed_points)
            self.separators[i][0].setPos(points[i])

        for i in range(len(self.separators)):
            self._update_fixed_points_separator(i)

    def point_is_occupied(self, x: float, y: float) -> tuple[bool, int]:
        """
        Check if the given point is occupied by existing separator and return the index of separator. Should be called
        when no Separator is moved. Should be called when exist at least one Separator.
        :param x: The x coordinate
        :param y: The y coordinate
        :return: A tuple. The first element is True if the point is occupied, False if not. The second element is the
        index of the separator if the position is occupied. If the position is not occupied, this second element will
        be the index of the separator before. A -1 will show an error.
        """
        # Find nearest available point
        real_y = find_nearest_point(self._get_y_values(), y)
        real_x = find_nearest_point(self._get_x_values(real_y), x)

        for i in range(len(self.separators)):
            if self.separators[i][0].is_on_the_border():
                if ((self.separators[i][0].complete_pos(True).x() == real_x and
                     self.separators[i][0].complete_pos(True).y() == real_y) or
                        (self.separators[i][0].complete_pos(False).x() == real_x and
                         self.separators[i][0].complete_pos(False).y() == real_y)):
                    return True, i
            else:
                if self.separators[i][0].complete_pos(True).x() == real_x and self.separators[i][0].complete_pos(
                        True).y() == real_y:
                    return True, i
            if self.separators[i][0].complete_pos(True).y() > real_y or \
                    (self.separators[i][0].complete_pos(True).y() == real_y and self.separators[i][0].complete_pos(
                        True).x() > real_x):
                return False, i - 1
        return True, -1

    def _find_free_point(self, x: float, y: float) -> tuple[float, float, int]:
        """
        Check if the given point is occupied by existing separator and if so, find another free point.
        The search goes from left to right and from up to down.
        :param x: The x coordinate
        :param y: The y coordinate
        :return: The same point if is free or new point if it is busy and the index of the previous separator. If there
                 are no points available, this function will return (None, None, -1)
        """
        # This auxiliary variable will reduce the search because all the separators with lower
        # indexes won't affect availability check
        is_occupied, index = self.point_is_occupied(x, y)
        if not is_occupied:
            real_y = find_nearest_point(self._get_y_values(), y)
            real_x = find_nearest_point(self._get_x_values(real_y), x)
            return real_x, real_y, index
        elif index != -1:
            pos = self.separators[index][0].complete_pos(True)
            real_y = pos.y()
            real_x = pos.x()

            for line in self._fixed_points:
                if line[0] >= real_y:
                    for i in range(len(line[1])):
                        if (line[0] == real_y and line[1][i][0] >= real_x) or line[0] > real_y:
                            if self.separators[index][0].is_on_the_border():
                                if not (i == 0 or i == len(line[1]) - 1):
                                    return line[1][i][0], line[0], index - 1
                                if i == 0:
                                    # If this position is busy, increment by one the ind in separators array
                                    index += 1
                            elif self.separators[index][0].complete_pos(True).x() == line[1][i][0] and \
                                    self.separators[index][0].complete_pos(True).y() == line[0]:
                                # If this position is busy, increment by one the ind in separators array
                                index += 1
                            else:
                                return line[1][i][0], line[0], index - 1
        return None, None, -1

    def add_limit_separators(self, first_limit_x: float, first_limit_y: float,
                             last_limit_x: float, last_limit_y: float) -> None:
        """
        This function add the limit separators to the canvas. Those separators are super Separators.
        :param first_limit_x: The x value of the initial Separator limit.
        :param first_limit_y: The y value of the initial Separator limit.
        :param last_limit_x: The x value of the last Separator limit.
        :param last_limit_y: The y value of the last Separator limit.
        """
        self.add_separator(first_limit_x, first_limit_y, True)
        self.add_separator(last_limit_x, last_limit_y, True)
        self.promote_separator(last_limit_x, last_limit_y)
        self.promote_separator(first_limit_x, first_limit_y)

    def add_separators_without_checking(self, points: list[tuple[QPointF, bool]]) -> None:
        """
        Add all the separators to the canvas without checking the validity of the positions.
        :param points: The separator points. The first element of each tuple is the position of the separator and the
                       second is a boolean that indicates if it is a super separator.
        """

        for point in points:
            # Create needed new elements
            new_separator = Separator(
                point[0].x(), point[0].y(), self._height, self._fixed_points, self.emitter, self._parent
            )
            self.separators.insert(-1, [new_separator, point[1]])
            if point[1]:
                new_separator.setPen(self._super_pen)
            else:
                new_separator.setPen(self._regular_pen)

        for i in range(1, len(self.separators) - 1):
            self.separators[i][0].set_fixed_points(
                self._set_fixed_points_subgroup(
                    self.separators[i - 1][0].complete_pos(True).x(),
                    self.separators[i - 1][0].complete_pos(True).y(),
                    self.separators[i + 1][0].complete_pos(False).x(),
                    self.separators[i + 1][0].complete_pos(False).y()
                )
            )

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
            real_y = find_nearest_point(self._get_y_values(), y)
            real_x = find_nearest_point(self._get_x_values(real_y), x)
            index = len(self.separators) - 1
            # Create needed new elements
            new_separator = Separator(
                real_x,
                real_y,
                self._height,
                self._fixed_points,
                None,
                self._parent

            )
        else:
            real_x, real_y, index = self._find_free_point(x, y)

            if (real_x is None and real_y is None) or index == -1:
                return False

            # Create needed new elements
            new_separator = Separator(
                real_x,
                real_y,
                self._height,
                self._set_fixed_points_for_new_separator(index),
                self.emitter,
                self._parent

            )

        new_separator.setPen(self._regular_pen)

        if is_static:
            new_separator.setFlags(new_separator.flags() & ~QGraphicsItem.ItemIsMovable)
            new_separator.setCursor(Qt.ArrowCursor)

        self.separators.insert(index + 1, [new_separator, False])

        self._update_fixed_points_separator(index)
        self._update_fixed_points_separator(index + 2)

        return True

    def delete_separator(self, x: float, y: float) -> bool:
        """
        Remove a separator.
        :param x: The x coordinate
        :param y: The y coordinate
        :return: True if success, False if error. There can be an error if the coordinates are out of bounds or if in
                 the given coordinates there is no separator
        """
        is_occupied, index = self.point_is_occupied(x, y)
        if not is_occupied:
            return False

        removed_separator = self.separators.pop(index)

        self._update_fixed_points_separator(index - 1)
        self._update_fixed_points_separator(index)

        self._parent.scene().removeItem(removed_separator[0])

        self.emitter.removed.emit(removed_separator[0])

        return True

    def delete_all_separators(self) -> None:
        """
        Remove all the separators.
        """
        for _ in range(len(self.separators)):
            removed_separator = self.separators.pop()
            self._parent.scene().removeItem(removed_separator[0])

    def promote_separator(self, x: float, y: float) -> bool:
        """
        Promote a separator to a super Separator.
        :param x: The x coordinate
        :param y: The y coordinate
        :return: True if success, False if error. There can be an error if the coordinates are out of bounds or if in
                 the given coordinates there is no separator
        """
        is_occupied, sep_index = self.point_is_occupied(x, y)
        if not is_occupied:
            return False

        if self.separators[sep_index][1]:
            return False

        self.separators[sep_index][1] = True

        self.separators[sep_index][0].setPen(self._super_pen)

        return True

    def demote_separator(self, x: float, y: float) -> bool:
        """
        Demote a super Separator to a normal separator.
        :param x: The x coordinate
        :param y: The y coordinate
        :return: True if success, False if error. There can be an error if the coordinates are out of bounds or if in
                 the given coordinates there is no separator
        """
        is_occupied, sep_index = self.point_is_occupied(x, y)
        if not is_occupied:
            return False

        if not self.separators[sep_index][1]:
            return False

        self.separators[sep_index][1] = False

        self.separators[sep_index][0].setPen(self._regular_pen)

        return True

    def is_super_separator(self, x: float, y: float) -> bool:
        """
        Check if in the given coordinates there is a super Separator.
        :param x: The x coordinate
        :param y: The y coordinate
        :return: True if success, False if error. There can be an error if the coordinates are out of bounds or if in
                 the given coordinates there is no separator
        """
        is_occupied, sep_index = self.point_is_occupied(x, y)
        if not is_occupied:
            return False

        return self.separators[sep_index][1]

    def _set_fixed_points_for_new_separator(self, index: int) -> list[tuple[float, list[tuple[float, bool]]]]:
        """
        Set the fixed points for a new created separator.
        :param index: Index of the element after which the new separator is to be inserted
        :return: The fixed_points structure for the new separator
        """
        start_x = self.separators[index][0].complete_pos(True).x()
        start_y = self.separators[index][0].complete_pos(True).y()

        end_x = self.separators[index + 1][0].complete_pos(False).x()
        end_y = self.separators[index + 1][0].complete_pos(False).y()
        return self._set_fixed_points_subgroup(start_x, start_y, end_x, end_y)

    def _set_fixed_points_subgroup(self,
                                   start_x: float, start_y: float,
                                   end_x: float, end_y: float
                                   ) -> list[tuple[float, list[tuple[float, bool]]]]:
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
        for line in self._fixed_points:
            if end_y >= line[0]:
                if line[0] >= start_y:
                    start_recording = True
                    for x_value in line[1]:
                        if ((line[0] == start_y and x_value[0] > start_x) or line[0] > start_y) and \
                                ((line[0] == end_y and x_value[0] < end_x) or line[0] < end_y):
                            if start_recording:
                                start_recording = False
                                new_fixed_points.append((line[0], []))
                            new_fixed_points[-1][1].append(x_value)
            else:
                break  # If left values are higher, end loop

        return new_fixed_points

    def _update_fixed_points_separator(self, index: int) -> None:
        """
        Update the fixed_points of the separator for a given index separator.
        :param index: Index of the separator
        """
        if (len(self.separators) - 2) >= index >= 1:
            self.separators[index][0].set_fixed_points(
                self._set_fixed_points_subgroup(
                    self.separators[index - 1][0].complete_pos(True).x(),
                    self.separators[index - 1][0].complete_pos(True).y(),
                    self.separators[index + 1][0].complete_pos(False).x(),
                    self.separators[index + 1][0].complete_pos(False).y()
                )
            )

    def _separator_is_released(self, separator: Separator) -> None:
        """
        Updates the fixed-points of the surrounding separators.
        :param separator: The separator that has been released.
        """
        only_separators = [e[0] for e in self.separators]
        self._update_fixed_points_separator(only_separators.index(separator) - 1)
        self._update_fixed_points_separator(only_separators.index(separator) + 1)

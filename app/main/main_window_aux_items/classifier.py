from typing import Any

import numpy as np
from PyQt5.QtCore import QPointF, QObject, pyqtSignal

from PyQt5.QtWidgets import QGraphicsItem

from .descriptor.descriptor_handler import DescriptorHandler
from .main_text import MainText
from .separator.separator_handler import SeparatorHandler
from .rounded_rect.rounded_rect_handler import RoundedRectHandler

from collections import Counter


def most_common(lst: list[str]) -> str:
    """
    Find the most common item in the list of strings. If there is a stalemate, the first most common element will be
    returned.
    :param lst: The list of strings.
    :return: The most common element.
    """
    data = Counter(lst)
    return data.most_common(1)[0][0]


def create_colors_dict(default_text: str, color_list: list[str], default_descriptor_value: str,
                       allowed_descriptor_values: list[str]) -> dict[str, str]:
    """
    Create a dictionary from a list of colors. This dictionary will have as a key of each element the color
    itself and as a value, a list containing the values of the different editable parts of the descriptor text.
    :param default_text: The text that is placed in the descriptors as default.
    :param color_list: The list with the colors.
    :param default_descriptor_value: The default editable part of the descriptor.
    :param allowed_descriptor_values: The allowed editable values of the descriptor.
    :return: The dictionary.
    """
    editable_texts_number = len(default_text.split(default_descriptor_value)) - 1
    allo_str_len = len(allowed_descriptor_values)

    if len(color_list) != np.power(allo_str_len, editable_texts_number) + 1:
        raise RuntimeError("There should be " + str(np.power(allo_str_len, editable_texts_number) + 1) +
                           " colors for classifier module but got " + str(len(color_list)) + " instead.")

    colors = {"": color_list[0]}

    for i in range(1, len(color_list)):
        value = ""
        for e in range(editable_texts_number):
            if e == editable_texts_number - 1:
                value += (str(e) + allowed_descriptor_values[(i - 1) % allo_str_len])
            else:
                value += (str(e) + allowed_descriptor_values[
                    np.floor_divide(i - 1, allo_str_len * (editable_texts_number - 1 - e)) % allo_str_len
                    ])
        colors[value] = color_list[i]
    return colors


def obtain_limit_points(points: list[tuple[float, list[list[float | str | bool]]]]
                        ) -> list[tuple[float, tuple[float, float]]]:
    """
    Obtain the limit x-values with its y-values from each lines from the structure that returns the MainText object.
    :param points: The points obtained from MainText object.
    :return: The limit points.
    """
    return [(i[0], (i[1][0][0], i[1][-1][0])) for i in points]


def obtain_separator_points(complete_points: list[tuple[float, list[list[float | str | bool]]]]
                            ) -> list[tuple[float, list[tuple[float, bool]]]]:
    """
    Extract from the complex structure that returns MainText object, the list of points with this structure:
    [(y_0, [(x_0, Ignored), (x_1, Ignored), ...]), (y_1, [(x_0, Ignored), (x_1, Ignored), ...]), ...]
    :return: The list with the points
    """
    return [(i[0], [(e[0], e[2]) for e in i[1]]) for i in complete_points]


def get_repos_sep_points(text_list: list[str],
                         complete_point_list: list[tuple[float, list[list[float | str | bool]]]]) -> list[QPointF]:
    """
    Reposition the separators to fit the new text format. The positions that the separators will occupy will be
    such that the groups of words that form these separators will be the same.
    :param text_list: A list with the groups of words made by the separators.
    :param complete_point_list: The list of all available points with its associated word.
    :return: The list of new positions for the Separators.
    """
    text_list_index = 0
    separator_points = [QPointF(complete_point_list[0][1][0][0], complete_point_list[0][0])]
    aux_text = ""

    for y_index in range(len(complete_point_list)):
        for x_index in range(len(complete_point_list[y_index][1])):
            if complete_point_list[y_index][1][x_index][1] != '':
                if complete_point_list[y_index][1][x_index][2]:
                    aux_text += complete_point_list[y_index][1][x_index][1]
                else:
                    aux_text += (" " + complete_point_list[y_index][1][x_index][1])

                # Do the comparison without the first space character
                if aux_text[1:] not in text_list[text_list_index]:
                    text_list_index += 1
                    aux_text = " " + complete_point_list[y_index][1][x_index][1]
                    separator_points.append(
                        QPointF(complete_point_list[y_index][1][x_index][0], complete_point_list[y_index][0])
                    )
    # Add last element
    separator_points.append(
        QPointF(complete_point_list[-1][1][-1][0], complete_point_list[-1][0])
    )
    return separator_points


def get_repos_sep_points_with_super_sep(sep_text_list: list[str], super_sep_text_list: list[str],
                                        complete_point_list: list[tuple[float, list[list[float | str | bool]]]]
                                        ) -> list[tuple[QPointF, bool]]:
    """
    Find the position of the separators that make those text lists. Also, indicates if a Separator is a super Separator
    based on super_sep_text_list.
    :param sep_text_list: The list with the groups of words made by the separators.
    :param super_sep_text_list: The list with the groups of words made by the super separators.
    :param complete_point_list: The list of all available points with its associated word.
    :return: The list of new positions for the Separators with a boolean per element that indicates if the Separator is
    a super Separator.
    """
    sep_text_list_index = 0
    super_sep_text_list_index = 0
    separator_points = [(QPointF(complete_point_list[0][1][0][0], complete_point_list[0][0]), False)]
    sep_aux_text = ""
    super_sep_aux_text = ""

    for y_index in range(len(complete_point_list)):
        for x_index in range(len(complete_point_list[y_index][1])):
            if complete_point_list[y_index][1][x_index][1] != '':
                if complete_point_list[y_index][1][x_index][2]:
                    sep_aux_text += complete_point_list[y_index][1][x_index][1]
                else:
                    sep_aux_text += (" " + complete_point_list[y_index][1][x_index][1])

                # Do the comparison without the first space character
                if sep_aux_text[1:] not in sep_text_list[sep_text_list_index]:
                    sep_text_list_index += 1
                    super_sep_aux_text += sep_aux_text[:-len(complete_point_list[y_index][1][x_index][1]) - 1]
                    sep_aux_text = " " + complete_point_list[y_index][1][x_index][1]

                    if (super_sep_aux_text[1:] + sep_aux_text) not \
                            in super_sep_text_list[super_sep_text_list_index]:
                        super_sep_aux_text = ""
                        super_sep_text_list_index += 1
                        separator_points.append(
                            (QPointF(complete_point_list[y_index][1][x_index][0], complete_point_list[y_index][0]),
                             True)
                        )
                    else:
                        separator_points.append(
                            (QPointF(complete_point_list[y_index][1][x_index][0], complete_point_list[y_index][0]),
                             False)
                        )
    # Add last element
    separator_points.append(
        (QPointF(complete_point_list[-1][1][-1][0], complete_point_list[-1][0]), False)
    )
    return separator_points


class ClassifierEmitter(QObject):
    classifier_has_changed = pyqtSignal()


class Classifier:
    """
    This class controls all the behaviour of the QGraphicsItems associated with the graphical text classification. That
    is, the rectangles and its descriptors and the separators between them. If any of the elements controlled by this
    object changes its position or value, a signal will be emitted indicating it.
    """

    def __init__(self, text: str, text_width: float, text_size: float, default_descriptor_string: str,
                 default_descriptor_value: str, allowed_descriptor_values: list[str], rect_colors: list[str],
                 regular_sep_color: str, super_sep_color: str, parent: QGraphicsItem) -> None:
        """
        Create Classifier object. Only one object form this class should be created
        :param text: The text to be analyzed.
        :param text_width: The maximum width of this element. Is determined by the max text width.
        :param text_size: The point text size. All the elements will adapt their size to this value to maintain always
                          the same proportion.
        :param default_descriptor_string: The default complete text that will appear in the descriptors.
        :param default_descriptor_value: The default value of editable parts of the descriptors.
        :param allowed_descriptor_values: The allowed values that can be the editable parts of the descriptors.
        :param rect_colors: The list of all the available background RoundedRect colors.
        :param regular_sep_color: A valid HTML color that will have the regular separators.
        :param super_sep_color: A valid HTML color that will have the super separators.
        :param parent: The QGraphicsItem parent of this element. Can't be None
        """
        self._default_descriptor_value = default_descriptor_value
        self._allowed_descriptor_values = allowed_descriptor_values

        self._text = MainText(text, text_size, text_width, 300, parent)

        complete_points = self._text.get_complete_points()
        sep_points = obtain_separator_points(complete_points)

        # Set separators
        self._sep_handler = SeparatorHandler(text_size * 2, sep_points, regular_sep_color, super_sep_color, parent)
        self._sep_handler.add_limit_separators(
            sep_points[0][1][0][0],
            sep_points[0][0],
            sep_points[-1][1][-1][0],
            sep_points[-1][0],
        )

        # Set separator width according to text size
        self._sep_handler.set_separator_width(max(1.0, text_size / 2.5))

        self._rects_handler = RoundedRectHandler(
            text_size * 2,
            text_size / 2,
            obtain_limit_points(complete_points),
            create_colors_dict(
                default_descriptor_string, rect_colors, self._default_descriptor_value, self._allowed_descriptor_values
            ),
            parent
        )
        self._rects_handler.add_separator_listeners(
            self._sep_handler.emitter.pos_changed,
            self._sep_handler.emitter.clicked_on_the_border,
            self._sep_handler.emitter.removed
        )

        self._descriptors_handler = DescriptorHandler(
            text_size * 2.4,
            default_descriptor_string,
            default_descriptor_value,
            allowed_descriptor_values,
            text_size * 2 / 3,
            obtain_limit_points(complete_points),
            parent
        )
        self._descriptors_handler.add_separator_listeners(
            self._sep_handler.emitter.pos_changed,
            self._sep_handler.emitter.clicked_on_the_border,
            self._sep_handler.emitter.removed
        )

        self._rects_handler.add_descriptor_listeners(self._descriptors_handler.emitter.editable_text_changed)

        self.emitter = ClassifierEmitter()
        self._sep_handler.emitter.released.connect(self._separator_is_released)
        self._descriptors_handler.emitter.editable_text_changed.connect(self._descriptor_changed)

    def get_text(self) -> str:
        """
        Obtain the plain text that is being analyzed.
        :return: The plain text.
        """
        return self._text.get_text()

    def set_colors(self, colors: list[str]) -> None:
        """
        Set the colors that will be used by the rounded rects depending on the value of the descriptor. The length
        of this list should be the same as the possible combinations of the descriptor text plus one (the default one).
        Also, the colors list should be of any HTML valid color.
        :param colors: List of all available colors
        """
        self._rects_handler.set_colors(create_colors_dict(
            self._descriptors_handler.get_default_text(),
            colors,
            self._default_descriptor_value,
            self._allowed_descriptor_values
        ))

    def set_default_descriptor(self, default_descriptor: str, colors: list[str]) -> None:
        """
        Set the default descriptor for all the descriptors. Should contain one or more "default_descriptor_value"
        characters. The list of colors will be the colors that the rounded rects will have depending on the value of the
        descriptor. The length of this list should be the same as the possible combinations of the descriptor text plus
        one (the default one). Also, the colors list should be of any HTML valid color.
        :param default_descriptor: The default string that will appear in the descriptor. Should contain one or more
                                   "default_descriptor_value" characters.
        :param colors: List of all available colors
        """
        self._descriptors_handler.set_default_text(default_descriptor, True)
        self._rects_handler.set_colors(create_colors_dict(
            default_descriptor, colors, self._default_descriptor_value, self._allowed_descriptor_values
        ))
        self.emitter.classifier_has_changed.emit()

    def get_default_descriptor(self) -> str:
        """
        Returns the default descriptor text used in all the descriptors.
        :return: The default descriptor as a string
        """
        return self._descriptors_handler.get_default_text()

    def get_text_size(self) -> int | float:
        """
        Return the text size.
        :return: The text size as a number.
        """
        return self._text.font().pointSize()

    def split(self, x: float, y: float) -> bool:
        """
        Splits the nearest rectangle to the given coordinates in two, placing a separator where the split has been made.
        :param x: The x coordinate
        :param y: The y coordinate
        :return: True if success, False if error. There can be a mistake if the coordinates are out of bounds or if
        there is no more space to place a separator
        """
        if self._sep_handler.add_separator(x, y, False):
            self.emitter.classifier_has_changed.emit()
            return True
        return False

    def join(self, x: float, y: float) -> bool:
        """
        Remove a separator and join the two remaining rectangles.
        :param x: The x coordinate
        :param y: The y coordinate
        :return: True if success, False if error. There can be a mistake if the coordinates are out of bounds or if in
        the given coordinates there is no separator
        """
        if self._sep_handler.delete_separator(x, y):
            self.emitter.classifier_has_changed.emit()
            return True
        return False

    def promote_separator(self, x: float, y: float) -> bool:
        """
        Promote the Separator in the given position to a super Separator.
        :param x: The x coordinate
        :param y: The y coordinate
        :return: True if success, False if error. There can be a mistake if the coordinates are out of bounds, if the
        separator is already a super Separator or if in the given coordinates there is no separator.
        """
        if self._sep_handler.promote_separator(x, y):
            self.emitter.classifier_has_changed.emit()
            return True
        return False

    def demote_separator(self, x: float, y: float) -> bool:
        """
        Demote the super Separator in the given position to a Separator.
        :param x: The x coordinate
        :param y: The y coordinate
        :return: True if success, False if error. There can be a mistake if the coordinates are out of bounds, if the
        separator is already a normal Separator or if in the given coordinates there is no separator.
        """
        if self._sep_handler.demote_separator(x, y):
            self.emitter.classifier_has_changed.emit()
            return True
        return False

    def is_super_separator(self, x: float, y: float) -> bool:
        """
        Checks if the Separator in the given position is a super Separator.
        :param x: The x coordinate
        :param y: The y coordinate
        :return: True if is a super Separator, False otherwise. There can be a mistake if the coordinates
                 are out of bounds or if in the given coordinates there is no separator
        """
        return self._sep_handler.is_super_separator(x, y)

    def there_is_a_separator(self, x: float, y: float) -> bool:
        """
        Check if the given point is occupied by existing separator. Should be called when no Separator is moved. Should
        be called when exist at least one Separator.
        :param x: The x coordinate
        :param y: The y coordinate
        :return: True if the point is occupied by a separator, False if not.
        """
        is_occupied, index = self._sep_handler.point_is_occupied(x, y)
        if is_occupied and (index != 0 and index != len(self._sep_handler.separators) - 1):
            return True
        return False

    def get_text_item_height(self) -> float:
        """
        This function return the number of pixels that will occupy vertically the text item.
        :return: The number of pixels that will occupy the text item
        """
        return self._text.boundingRect().height()

    def get_text_classified(self) -> list[str]:
        """
        Gets the subgroups of words that form the separators within the text.
        :return: A list with a group of words per element.
        """
        text = ""
        result = []
        sep_points = self._sep_handler.get_separator_points()

        # This ind will be used to access all the positions in separator_points
        sep_ind = 0

        complete_point_list = self._text.get_complete_points()

        for y_index in range(len(complete_point_list)):
            for x_index in range(len(complete_point_list[y_index][1])):
                if sep_ind < len(sep_points) and \
                        sep_points[sep_ind].x() == complete_point_list[y_index][1][x_index][0] and \
                        sep_points[sep_ind].y() == complete_point_list[y_index][0]:
                    result.append(text[1:])
                    sep_ind += 1
                    text = ""

                if complete_point_list[y_index][1][x_index][1] != '':
                    if complete_point_list[y_index][1][x_index][2] and text != "":
                        text += complete_point_list[y_index][1][x_index][1]
                    else:
                        text += (" " + complete_point_list[y_index][1][x_index][1])

        result.append(text[1:])

        return result

    def get_text_analyzed(self) -> list[tuple[list[tuple[str, str]], str]]:
        """
        Gets the subgroups of words that form the separators within the text and its descriptor tag. Also, obtain the
        tag for all the super separator groups.
        :return: A list of tuples with the text classified and analyzed. The first tuple element is a list with all the
        clauses between two super Separators analyzed and the second element of the tuple is the descriptor value of
        this super clause.
        """
        text = ""
        result = []
        group = []
        sep_points = self._sep_handler.get_separator_points()
        super_sep_points = self._sep_handler.get_super_separator_points()
        descriptors_list = self._descriptors_handler.get_descriptor_values()

        # This ind will be used to access all the positions in separator_points
        sep_ind = 0
        super_sep_ind = 0

        complete_point_list = self._text.get_complete_points()

        for y_index in range(len(complete_point_list)):
            for x_index in range(len(complete_point_list[y_index][1])):
                if sep_ind < len(sep_points) and \
                        sep_points[sep_ind].x() == complete_point_list[y_index][1][x_index][0] and \
                        sep_points[sep_ind].y() == complete_point_list[y_index][0]:
                    group.append((text[1:], descriptors_list[sep_ind]))
                    sep_ind += 1
                    text = ""
                if super_sep_ind < len(super_sep_points) and \
                        super_sep_points[super_sep_ind].x() == complete_point_list[y_index][1][x_index][0] and \
                        super_sep_points[super_sep_ind].y() == complete_point_list[y_index][0]:
                    super_sep_ind += 1
                    result.append((group, most_common([i[1] for i in group])))
                    group = []

                if complete_point_list[y_index][1][x_index][1] != '':
                    if complete_point_list[y_index][1][x_index][2] and text != "":
                        text += complete_point_list[y_index][1][x_index][1]
                    else:
                        text += (" " + complete_point_list[y_index][1][x_index][1])

        group.append((text[1:], descriptors_list[sep_ind]))
        result.append((group, most_common([i[1] for i in group])))

        return result

    def set_text(self, text) -> None:
        """
        Set the text to be analyzed as a plain text.
        :param text: The text that will appear.
        """
        self.emitter.classifier_has_changed.emit()

        self._text.set_text(text)
        complete_points = self._text.get_complete_points()
        sep_points = obtain_separator_points(complete_points)

        self._sep_handler.delete_all_separators()
        self._sep_handler.set_fixed_points(sep_points)
        self._sep_handler.add_limit_separators(
            sep_points[0][1][0][0],
            sep_points[0][0],
            sep_points[-1][1][-1][0],
            sep_points[-1][0],
        )

        limit_points = obtain_limit_points(complete_points)

        self._rects_handler.set_points(limit_points, [], True)
        self._descriptors_handler.set_points(limit_points, [], True)

    def set_text_size(self, text_size: float | int) -> None:
        """
        Set the text size. Also, the height of the separators and the rects and the text size of the descriptors is
        changed to maintain the proportion.
        :param text_size: The text size as a number.
        """
        self.emitter.classifier_has_changed.emit()

        # Save text_list from the original text_size to reposition all the separators
        text_list_previous_size = self.get_text_classified()

        # Set text size
        self._text.set_text_size(text_size)

        # Change rects, separators and descriptors_handler height
        self._sep_handler.set_separator_width(max(1.0, text_size / 2.5))
        self._sep_handler.set_separator_height(text_size * 2)

        self._rects_handler.set_height_and_radius(text_size * 2, text_size / 2)
        self._descriptors_handler.set_y_offset_and_text_size(text_size * 2.4, text_size * 2 / 3)

        # Reposition separators to the new text size
        complete_point_list = self._text.get_complete_points()

        separator_points = get_repos_sep_points(text_list_previous_size, complete_point_list)

        sep_points_without_limits = separator_points[1:-1]
        limit_points = obtain_limit_points(complete_point_list)
        self._rects_handler.set_points(limit_points, sep_points_without_limits, False)
        self._descriptors_handler.set_points(limit_points, sep_points_without_limits, False)

        self._sep_handler.set_fixed_points(obtain_separator_points(complete_point_list))
        self._sep_handler.set_separator_points(separator_points)

    def set_text_analyzed(self, sep_text_list: list[str], super_sep_text_list: list[str], default_descriptor: [str],
                          colors: list[str], labels: list[str], values: list[list[str]]) -> None:
        """
        Set the text to be analyzed as an already analyzed text.

        :param sep_text_list: A list with all clauses.
        :param super_sep_text_list: A list with all super clauses.
        :param default_descriptor: The default complete text that will appear in the descriptors.
        :param colors: The list of all the available background RoundedRect colors.
        :param labels: The list of all the non-editable parts of the descriptor. In the case of Semantics should be "SD"
                       and/or "SG".
        :param values: A list with all the editable parts for each group of descriptors.
        """
        self.set_text(" ".join(sep_text_list))

        complete_point_list = self._text.get_complete_points()

        separator_points = get_repos_sep_points_with_super_sep(sep_text_list, super_sep_text_list, complete_point_list)

        for i in range(1, len(separator_points) - 1):
            self.split(separator_points[i][0].x(), separator_points[i][0].y())
            if separator_points[i][1]:
                self.promote_separator(separator_points[i][0].x(), separator_points[i][0].y())

        self._rects_handler.reset_colors()
        self._rects_handler.set_colors(create_colors_dict(
            default_descriptor, colors, self._default_descriptor_value, self._allowed_descriptor_values
        ))
        self._descriptors_handler.set_default_text(default_descriptor, False)
        self._descriptors_handler.set_texts(labels, values)

    def set_width(self, width: float) -> None:
        """
        Set the width of the text. All the separators will be repositioned to get an expected result.
        :param width: The text width.
        """
        # Save text_list from the original text_size to reposition all the separators
        text_list_previous_size = self.get_text_classified()

        # Set text width
        self._text.set_width(width)

        # Reposition separators to the new text size
        complete_point_list = self._text.get_complete_points()

        separator_points = get_repos_sep_points(text_list_previous_size, complete_point_list)

        sep_points_without_limits = separator_points[1:-1]
        limit_points = obtain_limit_points(complete_point_list)
        self._rects_handler.set_points(limit_points, sep_points_without_limits, False)
        self._descriptors_handler.set_points(limit_points, sep_points_without_limits, False)

        self._sep_handler.set_fixed_points(obtain_separator_points(complete_point_list))
        self._sep_handler.set_separator_points(separator_points)

    def _separator_is_released(self, separator: Any) -> None:
        """
        Called when a separator is released. Emits a signal to notify a change in the classifier.
        :param separator: The separator that has been released. Non-relevant.
        """
        self.emitter.classifier_has_changed.emit()

    def _descriptor_changed(self, separator_index: int, editable_text_list: list[str]) -> None:
        """
        Called when the text of a descriptor has changed. Emits a signal to notify a change in the classifier.
        :param separator_index: Non-relevant.
        :param editable_text_list: Non-relevant.
        """
        self.emitter.classifier_has_changed.emit()

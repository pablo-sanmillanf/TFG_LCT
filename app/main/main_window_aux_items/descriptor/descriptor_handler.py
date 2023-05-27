import typing

from PyQt5 import QtGui
from PyQt5.QtCore import QPointF, pyqtSignal, QObject
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGraphicsTextItem, QGraphicsItem

from ..separator.separator import Separator
from .descriptor import Descriptor


def _exponentialSearchDescriptors(exp_list: list[list[Descriptor | float | float | float]], wanted_pos: QPointF) -> int:
    """
    Finds the descriptor that has the position wanted_pos using an exponential search.
    :param exp_list: The list of all descriptors to search for. Each element has more data but the only relevant element
    is the first.
    :param wanted_pos: The desire position as a QPointF.
    :return: The index in the list where the desired Descriptor is.
    """
    if exp_list[0][0].pos() == wanted_pos:
        return 0
    exp_index = 1
    while exp_index < len(exp_list) and (exp_list[exp_index][0].pos().y() <= wanted_pos.y() or
                                         (exp_list[exp_index][0].pos().y() == wanted_pos.y() and
                                          exp_list[exp_index][0].pos().x() <= wanted_pos.x())):
        exp_index = exp_index * 2

    bin_list = exp_list[int(exp_index / 2):min(exp_index, len(exp_list))]

    # Perform binary list
    first = 0
    last = len(bin_list) - 1
    bin_index = -1
    while (first <= last) and (bin_index == -1):
        mid = (first + last) // 2
        if bin_list[mid][0].pos() == wanted_pos:
            bin_index = mid
        else:
            if (wanted_pos.y() < bin_list[mid][0].pos().y()) or \
                    (wanted_pos.y() == bin_list[mid][0].pos().y() and wanted_pos.x() < bin_list[mid][0].pos().x()):
                last = mid - 1
            else:
                first = mid + 1
    return bin_index + int(exp_index / 2)


def _exponentialSearchSeparators(exp_list: list[list[Separator | int | QPointF]], wanted_index: int) -> int:
    """
    Finds the index in the list of index exp_list that has the same value that wanted_index using an exponential search.
    :param exp_list: The list to search for. Each element has more data but the only relevant element is the second.
    :param wanted_index: The desire index to find in exp_list.
    :return: The index in the list where the desired index is or the next higher value if the index is not in the list.
    """
    if exp_list[0][1] + 1 == wanted_index:
        return 0
    exp_index = 1
    while exp_index < len(exp_list) and exp_list[exp_index][1] + 1 <= wanted_index:
        exp_index = exp_index * 2

    bin_list = exp_list[int(exp_index / 2):min(exp_index, len(exp_list))]

    # Perform binary list
    first = 0
    last = len(bin_list) - 1
    bin_index = -1
    while (first <= last) and (bin_index == -1):
        mid = (first + last) // 2
        if bin_list[mid][1] + 1 == wanted_index:
            bin_index = mid
        else:
            if wanted_index < bin_list[mid][1] + 1:
                last = mid - 1
            else:
                first = mid + 1
    if first > last:
        return last + int(exp_index / 2)
    else:
        return bin_index + int(exp_index / 2)


class DescriptorEmitter(QObject):
    editable_text_changed = pyqtSignal(int, list)


class DescriptorHandler:
    """
    This class handles the position and the content of all the Descriptors and emits a signal when the text of a group
    of descriptors has been changed. All the Descriptors between two Separators are considered a group of Descriptors
    and this class ensures that they have the same text and change when a Descriptor of the group changes.
    """
    _descriptors: list[list[Descriptor | float | float | float]]
    _separators: list[list[Separator | int | QPointF]]

    def __init__(self, y_offset: int | float, default_text: str, text_separator: str, allowed_strings: list[str],
                 text_size: float | int, points: list[tuple[float | int, tuple[float | int, float | int]]],
                 parent: QGraphicsItem, font: QFont = None) -> None:
        """
        Create DescriptorHandler object. Should be only one of this object.
        :param y_offset: Set y offset for all the positions calculated.
        :param default_text: The default text that will appear in the descriptor.
        :param text_separator: The part of the text in the Descriptor that will be substituted by a valid value.
        :param allowed_strings: A list of string with the valid values for the Descriptor.
        :param text_size: The size of the text as a point size.
        :param points: A list of points to correctly set the position of the descriptor. Each element is a tuple of
                       (Y-value, (X-left, X-Right)) where the x-value of the descriptor will be the one that will set
                       the Descriptor in the middle of X-left and X-Right.
        :param parent: The QGraphicsItem parent of this Separator. Can't be None
        :param font: The Descriptor's text font.
        """
        self.emitter = DescriptorEmitter()
        self._parent = parent
        self._y_offset = y_offset
        self._default_text = default_text
        self._text_separator = text_separator
        self._allowed_strings = allowed_strings

        if font is None:
            self._font = QGraphicsTextItem().font()
        else:
            self._font = font

        self._descriptors = []

        for i in range(len(points)):
            desc = Descriptor(default_text, self._text_separator, self._allowed_strings, parent, font)
            # [Descriptor, Y_Value_Without_Offset, Left_X_Value, Right_X_Value]
            self._descriptors.append([desc, points[i][0], points[i][1][0], points[i][1][-1]])
            self._set_descriptor_pos(i)
            desc.editable_text_changed.connect(self._text_changed)

        self._separators = []

        self.set_text_size(text_size)

    def set_default_text(self, default_text: str) -> None:
        """
        Changes the default text of the handler. This not change the default text of the Descriptors automatically.
        :param default_text: The default text string.
        """
        self._default_text = default_text

    def get_default_text(self) -> str:
        """
        Returns the default text of the handler.
        :return: The default text string.
        """
        return self._default_text

    def add_separator_listeners(self, pos_changed_fn: typing.Any, clicked_on_the_border_fn: typing.Any,
                                removed_fn: typing.Any) -> None:
        """
        Set the separator listeners of the handler.
        :param pos_changed_fn: This signal will be emitted when a separator is moved.
        :param clicked_on_the_border_fn: This signal will be emitted when a separator is clicked when is on the border
                                         of a line.
        :param removed_fn: This signal will be emitted when a separator is removed.
        """
        pos_changed_fn.connect(self._separator_position_changed)
        clicked_on_the_border_fn.connect(self._separator_clicked_on_the_border)
        removed_fn.connect(self._separator_removed)

    def _set_points_for_new_text(self, points: list[tuple[float, tuple[float, float]]],
                                 descriptor_text: tuple[list[str], list[str], int, bool, str]) -> None:
        """
        Set the position and the text for the descriptors when the text is new.
        :param points: The points for the descriptors. Each element is a tuple of (Y-value, (X-left, X-Right)) where the
                       x-value of the descriptor will be the one that will set the Descriptor in the middle of X-left
                       and X-Right.
        :param descriptor_text: The info to use in paste_text() Descriptor function
        """
        if len(points) > len(self._descriptors):  # We need to create more descriptors
            desc_index = 0
            for desc_index in range(len(self._descriptors)):
                self._descriptors[desc_index][1] = points[desc_index][0]
                self._descriptors[desc_index][2] = points[desc_index][1][0]
                self._descriptors[desc_index][3] = points[desc_index][1][1]
                self._descriptors[desc_index][0].paste_text(descriptor_text)
                self._set_descriptor_pos(desc_index)
            for e in range(desc_index + 1, len(points)):
                desc = Descriptor(
                    self._default_text, self._text_separator, self._allowed_strings, self._parent, self._font
                )
                # [Descriptor, Y_Value_Without_Offset, Left_X_Value, Right_X_Value]
                self._descriptors.append([desc, points[e][0], points[e][1][0], points[e][1][-1]])
                self._descriptors[e][0].paste_text(descriptor_text)
                self._set_descriptor_pos(e)
                desc.editable_text_changed.connect(self._text_changed)

        else:  # We need to delete part of existing descriptors
            desc_index = 0
            for desc_index in range(len(points)):
                self._descriptors[desc_index][1] = points[desc_index][0]
                self._descriptors[desc_index][2] = points[desc_index][1][0]
                self._descriptors[desc_index][3] = points[desc_index][1][1]
                self._descriptors[desc_index][0].paste_text(descriptor_text)
                self._set_descriptor_pos(desc_index)
            for _ in range(desc_index + 1, len(self._descriptors)):
                removed_descriptor = self._descriptors.pop()
                self._parent.scene().removeItem(removed_descriptor[0])

    def set_points(self, points: list[tuple[float, tuple[float, float]]], separator_points: list[QPointF],
                   new_text: bool) -> None:
        """
        Set the position and the text for the descriptors.
        :param points: The points for the descriptors. Each element is a tuple of (Y-value, (X-left, X-Right)) where the
                       x-value of the descriptor will be the one that will set the Descriptor in the middle of X-left
                       and X-Right.
        :param separator_points: A list with the separator positions. If the text is new, this list should be empty.
        :param new_text: A boolean that indicates if the text is new.
        """

        descriptor_texts_list = []
        if new_text:
            self._separators.clear()
            descriptor_texts_list.append(
                Descriptor(self._default_text, self._text_separator, self._allowed_strings, None, self._font).copy_text()
            )
        else:
            if len(separator_points) != len(self._separators):
                raise RuntimeError("There are not the same points as separators in set_points() function")

            for sep in self._separators:
                descriptor_texts_list.append(self._descriptors[sep[1]][0].copy_text())
            descriptor_texts_list.append(self._descriptors[-1][0].copy_text())

        if len(separator_points) == 0:
            self._set_points_for_new_text(points, descriptor_texts_list[0])
        else:
            self._set_points_with_separators(points, separator_points, descriptor_texts_list)

    def _set_points_with_separators(self, points: list[tuple[float, tuple[float, float]]],
                                    separator_points: list[QPointF],
                                    descriptor_texts_list: list[tuple[list[str], list[str], int, bool, str]]) -> None:
        """
        Set the position and the text for the descriptors.
        :param points: The points for the descriptors. Each element is a tuple of (Y-value, (X-left, X-Right)) where the
                       x-value of the descriptor will be the one that will set the Descriptor in the middle of X-left
                       and X-Right.
        :param separator_points: A list with the separator positions.
        :param descriptor_texts_list: A list with the info to use in paste_text() Descriptor function for each group of
                                      Descriptors.
        """

        if len(separator_points) + len(points) > len(self._descriptors):  # We need to create more descriptors
            desc_index = 0
            sep_index = 0
            points_index = 0
            sep_find = False
            for desc_index in range(len(self._descriptors)):
                self._descriptors[desc_index][1] = points[points_index][0]
                if sep_find:
                    self._descriptors[desc_index][2] = separator_points[sep_index].x()
                    sep_find = False
                    sep_index += 1
                else:
                    self._descriptors[desc_index][2] = points[points_index][1][0]

                if sep_index < len(separator_points) and (
                        separator_points[sep_index].y() == points[points_index][0] and
                        separator_points[sep_index].x() <= points[points_index][1][1]):
                    self._descriptors[desc_index][3] = separator_points[sep_index].x()

                    # Update separators
                    self._separators[sep_index][1] = desc_index
                    self._separators[sep_index][2] = separator_points[sep_index]
                    sep_find = True
                else:
                    self._descriptors[desc_index][3] = points[points_index][1][1]
                    points_index += 1

                self._descriptors[desc_index][0].paste_text(descriptor_texts_list[sep_index])
                self._set_descriptor_pos(desc_index)
            for e in range(desc_index + 1, len(separator_points) + len(points)):
                desc = Descriptor(
                    self._default_text, self._text_separator, self._allowed_strings, self._parent, self._font
                )

                if sep_find:
                    left_x = separator_points[sep_index].x()
                    sep_find = False
                    sep_index += 1
                else:
                    left_x = points[points_index][1][0]

                if sep_index < len(separator_points) and (
                        separator_points[sep_index].y() == points[points_index][0] and
                        separator_points[sep_index].x() <= points[points_index][1][1]):
                    right_x = separator_points[sep_index].x()

                    # Update separators
                    self._separators[sep_index][1] = desc_index
                    self._separators[sep_index][2] = separator_points[sep_index]
                    sep_find = True
                else:
                    right_x = points[points_index][1][1]
                    points_index += 1

                desc.paste_text(descriptor_texts_list[sep_index])

                # [Descriptor, Y_Value_Without_Offset, Left_X_Value, Right_X_Value]
                self._descriptors.append([desc, points[points_index - 1][0], left_x, right_x])

                self._set_descriptor_pos(e)
                desc.editable_text_changed.connect(self._text_changed)

        else:  # We need to delete part of existing descriptors
            desc_index = 0
            sep_index = 0
            points_index = 0
            sep_find = False
            for desc_index in range(len(separator_points) + len(points)):

                self._descriptors[desc_index][1] = points[points_index][0]
                if sep_find:
                    self._descriptors[desc_index][2] = separator_points[sep_index].x()
                    sep_find = False
                    sep_index += 1
                else:
                    self._descriptors[desc_index][2] = points[points_index][1][0]

                if sep_index < len(separator_points) and (
                        separator_points[sep_index].y() == points[points_index][0] and
                        separator_points[sep_index].x() <= points[points_index][1][1]):
                    self._descriptors[desc_index][3] = separator_points[sep_index].x()

                    # Update separators
                    self._separators[sep_index][1] = desc_index
                    self._separators[sep_index][2] = separator_points[sep_index]
                    sep_find = True
                else:
                    self._descriptors[desc_index][3] = points[points_index][1][1]
                    points_index += 1

                self._descriptors[desc_index][0].paste_text(descriptor_texts_list[sep_index])
                self._set_descriptor_pos(desc_index)

            for _ in range(desc_index + 1, len(self._descriptors)):
                removed_descriptor = self._descriptors.pop()
                self._parent.scene().removeItem(removed_descriptor[0])

    def _set_descriptor_pos(self, ind: int) -> None:
        """
        Sets the position of a specific Descriptor. If the X-left and the X-Right of the Descriptor are the same, hides
        the Descriptor.
        :param ind: Index of the Descriptor to set the position.
        """
        self._descriptors[ind][0].setPos(
            (self._descriptors[ind][3] +
             self._descriptors[ind][2] -
             self._descriptors[ind][0].boundingRect().width()) / 2,
            self._descriptors[ind][1] + self._y_offset
        )
        if self._descriptors[ind][3] == self._descriptors[ind][2]:
            self._descriptors[ind][0].hide()
        else:
            self._descriptors[ind][0].show()

    def set_default_text(self, default_text: str) -> None:
        """
        Set the default text for all the descriptors.
        :param default_text: The default text that will appear in the descriptor.
        """
        self._default_text = default_text
        for i in range(len(self._descriptors)):
            self._descriptors[i][0].set_default_text(default_text)

            self._set_descriptor_pos(i)

    def set_y_offset_and_text_size(self, y_offset: float, text_size: float) -> None:
        """
        Change the _y_offset and the text size for all the Descriptors.
        :param y_offset: The y offset in the Y position.
        :param text_size: The point size.
        """
        self._y_offset = y_offset
        self.set_text_size(text_size)

    def set_text_size(self, text_size: float | int) -> None:
        """
        Set the text size.
        :param text_size: The text size as a number.
        """
        font = self._font
        font.setPointSize(int(text_size))

        self.setFont(font)

    def setFont(self, font: QtGui.QFont) -> None:
        """
        Set text with a given font.
        :param font: The font object
        """
        self._font = font

        for i in range(len(self._descriptors)):
            self._descriptors[i][0].setFont(font)

            self._set_descriptor_pos(i)

    def set_texts(self, labels: list[str], values: list[list[str]]) -> None:
        """
        Set the texts for all the group of Descriptors.
        :param labels: Labels of the text. This corresponds to the non-editable part of the text except the ";"
                       character that is introduced by this function to separate the different parts of the text.
        :param values: The values of the editable part of the text for each group of Descriptors.
        """
        for i in range(1, len(labels)):
            labels[i] = ";" + labels[i]
        labels.append("")
        for i in range(len(self._separators)):
            self._descriptors[self._separators[i][1]][0].set_text(labels, values[i])
        self._descriptors[-1][0].set_text(labels, values[-1])

    def get_descriptor_values(self) -> list[str]:
        """
        Obtain the texts descriptors for all the clauses in a list.
        :return: The list of the texts descriptors.
        """
        text_list = []
        for sep in self._separators:
            text_list.append(self._descriptors[sep[1]][0].toPlainText())
        text_list.append(self._descriptors[-1][0].toPlainText())
        return text_list

    def _find_separator(self, separator: Separator) -> int:
        """
        Find the index of the given separator in self.separators.
        :param separator: The separator to look for.
        :return: The index of the separator.
        """
        for i in range(len(self._separators)):
            if self._separators[i][0] is separator:
                return i

    def _add_separator(self, separator: Separator, point: QPointF) -> None:
        """
        Add a separator to the list of separators and create a new Descriptor to use in the newly created group of
        Descriptors.
        :param separator: The created separator.
        :param point: The last position of the new created separator.
        """
        index_before = self._insert_descriptor(point)

        if len(self._separators) == 0:
            self._separators.append([separator, index_before, point])

            # Update text for the new group of descriptors
            self._descriptors[index_before + 1][0].emit_text_changed(False)
        else:
            for i in range(len(self._separators)):
                if (point.y() < self._separators[i][0].pos().y() or
                        (point.y() == self._separators[i][0].pos().y() and
                         point.x() < self._separators[i][0].pos().x())):
                    # [Separator, Last_index_before, Last_position]
                    self._separators.insert(i, [separator, index_before, point])

                    # Update "Last_index_before" for the separators after this separator
                    for e in range(i + 1, len(self._separators)):
                        self._separators[e][1] += 1

                    # Update text for the new group of descriptors
                    self._descriptors[index_before + 1][0].emit_text_changed(False)
                    return

            # If the separator is inserted after the last separator
            self._separators.append([separator, index_before, point])

            # Update text for the new group of descriptors
            self._descriptors[index_before + 1][0].emit_text_changed(False)

    def _insert_descriptor(self, point: QPointF) -> int:
        """
        Insert a new Descriptor when a separator is created in the self.descriptors structure and return the index of
        the previous Separator.
        :param point: The position of the newly created separator.
        :return: The index of the separator before the Descriptor.
        """
        for i in range(len(self._descriptors)):
            if (point.y() < self._descriptors[i][1] or
                    (point.y() == self._descriptors[i][1] and point.x() < self._descriptors[i][2])):
                self._descriptors.insert(
                    i,
                    [
                        Descriptor(
                            self._default_text, self._text_separator, self._allowed_strings, self._parent, self._font
                        ),
                        point.y(),
                        point.x(),
                        self._descriptors[i - 1][3]
                    ]
                )
                self._set_descriptor_pos(i)
                self._descriptors[i][0].editable_text_changed.connect(self._text_changed)

                self._descriptors[i - 1][3] = point.x()
                self._set_descriptor_pos(i - 1)

                return i - 1

        self._descriptors.append(
            [
                Descriptor(self._default_text, self._text_separator, self._allowed_strings, self._parent, self._font),
                point.y(),
                point.x(),
                self._descriptors[-1][3]
            ]
        )
        self._set_descriptor_pos(-1)
        self._descriptors[-1][0].editable_text_changed.connect(self._text_changed)

        self._descriptors[-2][3] = point.x()
        self._set_descriptor_pos(-2)

        return len(self._descriptors) - 2

    def _update_downwards(self, index: int, point: QPointF) -> int:
        """
        Update the position of a Descriptor group when a Separator is moved downwards.
        :param index: Index of the updated separator.
        :param point: The current position of the updated Separator.
        :return: The index of the first Descriptor in this Descriptor group.
        """
        for i in range(index, len(self._descriptors)):
            if point.y() > self._descriptors[i][1]:
                self._descriptors[i][3] = self._descriptors[i + 1][3]
                self._set_descriptor_pos(i)

                self._descriptors[i + 1][1] = self._descriptors[i + 2][1]
                self._descriptors[i + 1][2] = self._descriptors[i + 2][2]
                self._descriptors[i + 1][0].paste_text(self._descriptors[i][0].copy_text())
            else:
                self._descriptors[i + 1][2] = point.x()
                self._descriptors[i + 1][1] = self._descriptors[i][1]
                self._set_descriptor_pos(i + 1)

                self._descriptors[i][3] = point.x()
                self._set_descriptor_pos(i)
                return i
        raise RuntimeError("DOWNWARDS FINISH WITHOUT RETURNING")

    def _update_upwards(self, index: int, point: QPointF) -> int:
        """
        Update the position of a Descriptor group when a Separator is moved upwards.
        :param index: Index of the updated separator.
        :param point: The current position of the updated Separator.
        :return: The index of the first Descriptor in this Descriptor group.
        """
        for i in range(index, -1, -1):
            if point.y() < self._descriptors[i][1]:

                self._descriptors[i + 1][1] = self._descriptors[i][1]
                self._descriptors[i + 1][2] = self._descriptors[i][2]
                self._set_descriptor_pos(i + 1)

                self._descriptors[i][3] = self._descriptors[i - 1][3]
                self._descriptors[i][0].paste_text(self._descriptors[i + 1][0].copy_text())
            else:
                self._descriptors[i + 1][1] = self._descriptors[i][1]
                self._descriptors[i + 1][2] = point.x()
                self._set_descriptor_pos(i + 1)

                self._descriptors[i][3] = point.x()
                self._set_descriptor_pos(i)
                return i
        raise RuntimeError("UPWARDS FINISH WITHOUT RETURNING")

    def _separator_position_changed(self, moved_separator: QGraphicsItem, point: QPointF) -> None:
        """
        Updates the positions of the Descriptors affected by the movement of moved_separator. This function
        should be called every time a Separator has moved.
        :param moved_separator: The separator that has moved.
        :param point: The current position of the separator.
        """
        sep_index = self._find_separator(moved_separator)

        if sep_index is None:
            self._add_separator(moved_separator, point)
        else:
            if (point.y() < self._separators[sep_index][2].y() or
                    (point.y() == self._separators[sep_index][2].y() and
                     point.x() < self._separators[sep_index][2].x())):  # Separator moved upwards
                self._separators[sep_index][1] = self._update_upwards(self._separators[sep_index][1], point)

            elif (point.y() > self._separators[sep_index][2].y() or
                  (point.y() == self._separators[sep_index][2].y() and
                   point.x() > self._separators[sep_index][2].x())):  # Separator moved downwards
                self._separators[sep_index][1] = self._update_downwards(self._separators[sep_index][1], point)

            self._separators[sep_index][2] = point

    def _separator_clicked_on_the_border(self, moved_separator: QGraphicsItem, cursor_point: QPointF,
                                         right_point: QPointF, left_point: QPointF) -> None:
        """
        This function update Descriptor positions when a Separator that is on the border is clicked because when the
        separator is on the border, a copy of it appears at the end of the previous line (if it is on the left border)
        or at the beginning of the next line (if it is on the right border) and both copies are also selectable.

        :param moved_separator: The separator that has moved.
        :param cursor_point: The position of the cursor when the separator was clicked.
        :param right_point: The right position of the separator.
        :param left_point: The left position of the separator.
        """
        sep_index = self._find_separator(moved_separator)

        if sep_index is None:
            self._add_separator(moved_separator, right_point)
        else:
            # If the user released the separator in the right border and now the user is clicking in the left border
            # if self.separators[sep_index][2] == right_point and \
            #        (cursor_point - right_point).manhattanLength() > (cursor_point - left_point).manhattanLength():
            # Nothing is done because of the way function "update_downwards" is designed.

            # If the user released the separator in the left border and now the user is clicking in the right border
            if self._separators[sep_index][2] == left_point and \
                    (cursor_point - left_point).manhattanLength() > (cursor_point - right_point).manhattanLength():
                # Auxiliary variable to add clarity
                ind = self._separators[sep_index][1]

                self._descriptors[ind][1] = self._descriptors[ind - 1][1]
                self._descriptors[ind][2] = self._descriptors[ind - 1][3]
                self._descriptors[ind][3] = self._descriptors[ind - 1][3]
                self._set_descriptor_pos(ind)

                self._separators[sep_index][1] -= 1

                # Update text for this group of descriptors
                self._descriptors[ind + 1][0].emit_text_changed(False)

    def _separator_removed(self, separator: Separator) -> None:
        """
        Updates the number and position of the Descriptors when a Separator is removed.
        :param separator: The removed Separator.
        """
        # Get indexes
        sep_index = self._find_separator(separator)
        desc_index = self._separators[sep_index][1]

        # Remove separator and descriptor
        self._separators.pop(sep_index)
        removed_descriptor = self._descriptors.pop(desc_index + 1)

        # Update "Last_index_before" for the separators after this separator
        for e in range(sep_index, len(self._separators)):
            self._separators[e][1] -= 1

        # Update remaining descriptors
        self._descriptors[desc_index][3] = removed_descriptor[3]
        self._set_descriptor_pos(desc_index)

        # Update text for the new group of descriptors
        self._descriptors[desc_index][0].emit_text_changed(False)

        self._parent.scene().removeItem(removed_descriptor[0])

    def _text_changed(self, changed_descriptor: Descriptor, text_changed: bool) -> None:
        """
        This function handles the events when a Descriptor has changed, updating the text of all the Descriptors in the
        same group and sending a signal when the text has been modified.
        :param changed_descriptor: The Descriptor that has changed its text.
        :param text_changed: A boolean that indicates if the text has changed.
        """
        # Find changed descriptor using exponential search
        desc_index = _exponentialSearchDescriptors(self._descriptors, changed_descriptor.pos())

        # Find separator before the group of descriptors using exponential search
        sep_index = -1
        if len(self._separators) != 0:
            sep_index = _exponentialSearchSeparators(self._separators, desc_index)

        # Adapt bounds
        if sep_index == -1:
            start = 0
        else:
            start = self._separators[sep_index][1] + 1

        if sep_index == len(self._separators) - 1:
            end = len(self._descriptors)
        else:
            end = self._separators[sep_index + 1][1] + 1

        # Update text for the rest of the descriptors of the same group
        for i in range(start, end):
            self._descriptors[i][0].paste_text(self._descriptors[desc_index][0].copy_text())
            self._set_descriptor_pos(i)

        # Emit text changed signal
        if text_changed:
            self.emitter.editable_text_changed.emit(
                sep_index, self._descriptors[desc_index][0].get_editable_text_list()
            )

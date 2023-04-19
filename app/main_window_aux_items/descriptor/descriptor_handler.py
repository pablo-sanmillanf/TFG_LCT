import typing

from PyQt5 import QtGui
from PyQt5.QtCore import QPointF, pyqtSignal, QObject
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGraphicsTextItem, QGraphicsItem

from ..separator.separator import Separator
from .descriptor import Descriptor


def exponentialSearchDescriptors(exp_list: list[list[Descriptor | float | float | float]], wanted_pos: QPointF) -> int:
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
    return bin_index + int(exp_index/2)


def exponentialSearchSeparators(exp_list: list[list[Separator | int | QPointF]], wanted_index: int) -> int:
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
        return bin_index + int(exp_index/2)


class DescriptorEmitter(QObject):
    editable_text_changed = pyqtSignal(int, list)


class DescriptorHandler:
    """
    This class is a variant of QGraphicsTextItem that is used to set the value of a clause. Those values
    should be SD++, SD+, SD-, SD-- and/or SG--, SG-, SG+, SG++
    """
    descriptors: list[list[Descriptor | float | float | float]]
    separators: list[list[Separator | int | QPointF]]
    padding_height: float

    def __init__(self, y_offset: int | float, default_text: str, text_size: float | int,
                 points: list[tuple[float | int, tuple[float | int, float | int]]], parent: QGraphicsItem,
                 font: QFont = None) -> None:
        """
        Create Descriptor object.
        :param y_offset: Set y offset for all the points calculated.
        :param default_text: The default text that will appear in the descriptor.
        :param text_size: The size of the text as a point size.
        :param parent: The QGraphicsItem parent of this Separator. Can't be None
        :param font: The Descriptor's text font.
        """
        self.emitter = DescriptorEmitter()
        self.parent = parent
        self.y_offset = y_offset
        self.default_text = default_text

        if font is None:
            self.font = QGraphicsTextItem().font()
        else:
            self.font = font

        self.descriptors = []
        self.padding_height = self.get_separator_offsets_height()

        for i in range(len(points)):
            desc = Descriptor(default_text, parent, font)
            # [Descriptor, Y_Value_Without_Offset, Left_X_Value, Right_X_Value]
            self.descriptors.append([desc, points[i][0], points[i][1][0], points[i][1][-1]])
            self.set_descriptor_pos(i)
            desc.editable_text_changed.connect(self.text_changed)

        self.separators = []

        self.set_text_size(text_size)

    def add_separator_listeners(self, pos_changed_fn: typing.Any, clicked_on_the_border_fn: typing.Any) -> None:
        pos_changed_fn.connect(self.separator_position_changed)
        clicked_on_the_border_fn.connect(self.separator_clicked_on_the_border)

    def set_descriptor_pos(self, ind):
        rect = self.descriptors[ind][0].boundingRect()
        self.descriptors[ind][0].setPos(
            (self.descriptors[ind][3] + self.descriptors[ind][2] - rect.width()) / 2,
            self.descriptors[ind][1] + self.y_offset + self.padding_height + rect.height()
        )
        if self.descriptors[ind][3] == self.descriptors[ind][2]:
            self.descriptors[ind][0].hide()
        else:
            self.descriptors[ind][0].show()

    def set_default_text(self, default_text: str) -> None:
        """
        Set the default text for this descriptor.
        :param default_text: The default text that will appear in the descriptor.
        """
        for i in range(len(self.descriptors)):
            self.descriptors[i][0].set_default_text(default_text)

            self.set_descriptor_pos(i)

    def get_separator_offsets_height(self) -> float:
        """
        This function gets the height in pixels of the padding introduced by the QGraphicsTextItem
        element. To do so,the following system of equations must be solved:
            - padding + strip + padding = height_1
            - padding + strip + strip + padding = height_2
        Those values will be used to place the text

        :return: The padding height introduced by QGraphicsTextItem.
        """
        aux = QGraphicsTextItem()
        aux.setFont(self.font)

        aux.setHtml('<p align="justify">Test</p>')
        height_1 = aux.boundingRect().height()

        aux.setHtml('<p align="justify">Test<br>Test</p>')
        height_2 = aux.boundingRect().height()

        return height_1 - height_2 / 2

    def set_text_size(self, text_size: float | int) -> None:
        """
        Set the text size.
        :param text_size: The text size as a number.
        """
        font = self.font
        font.setPointSize(int(text_size))

        self.setFont(font)

    def setFont(self, font: QtGui.QFont) -> None:
        """
        Set text with a given font.
        :param font: The font object
        """
        self.font = font
        self.padding_height = self.get_separator_offsets_height()

        for i in range(len(self.descriptors)):
            self.descriptors[i][0].setFont(font)

            self.set_descriptor_pos(i)

    def find_separator(self, separator: Separator) -> int:
        for i in range(len(self.separators)):
            if self.separators[i][0] is separator:
                return i

    def add_separator(self, separator: Separator, point: QPointF):
        index_before = self.insert_descriptor(point)

        if len(self.separators) == 0:
            self.separators.append([separator, index_before, point])

            # Update text for the new group of descriptors
            self.descriptors[index_before + 1][0].emit_text_changed(False)
        else:
            for i in range(len(self.separators)):
                if (point.y() < self.separators[i][0].pos().y() or
                        (point.y() == self.separators[i][0].pos().y() and
                         point.x() < self.separators[i][0].pos().x())):
                    # [Separator, Last_index_before, Last_position]
                    self.separators.insert(i, [separator, index_before, point])

                    # Update "Last_index_before" for the separators after this separator
                    for e in range(i + 1, len(self.separators)):
                        self.separators[e][1] += 1

                    # Update text for the new group of descriptors
                    self.descriptors[index_before + 1][0].emit_text_changed(False)
                    return

            # If the separator is inserted after the last separator
            self.separators.append([separator, index_before, point])

            # Update text for the new group of descriptors
            self.descriptors[index_before + 1][0].emit_text_changed(False)

    def insert_descriptor(self, point: QPointF):

        for i in range(len(self.descriptors)):
            if (point.y() < self.descriptors[i][1] or
                    (point.y() == self.descriptors[i][1] and point.x() < self.descriptors[i][2])):
                self.descriptors.insert(
                    i,
                    [
                        Descriptor(self.default_text, self.parent, self.font),
                        point.y(),
                        point.x(),
                        self.descriptors[i - 1][3]
                    ]
                )
                self.set_descriptor_pos(i)
                self.descriptors[i][0].editable_text_changed.connect(self.text_changed)

                self.descriptors[i - 1][3] = point.x()
                self.set_descriptor_pos(i - 1)

                return i - 1

        self.descriptors.append(
            [
                Descriptor(self.default_text, self.parent, self.font),
                point.y(),
                point.x(),
                self.descriptors[-1][3]
            ]
        )
        self.set_descriptor_pos(-1)
        self.descriptors[-1][0].editable_text_changed.connect(self.text_changed)

        self.descriptors[-2][3] = point.x()
        self.set_descriptor_pos(-2)

        return len(self.descriptors) - 2

    def update_downwards(self, index, point: QPointF):
        for i in range(index, len(self.descriptors)):
            if point.y() > self.descriptors[i][1]:
                self.descriptors[i][3] = self.descriptors[i + 1][3]
                self.set_descriptor_pos(i)

                self.descriptors[i + 1][1] = self.descriptors[i + 2][1]
                self.descriptors[i + 1][2] = self.descriptors[i + 2][2]
                self.descriptors[i + 1][0].paste_text(self.descriptors[i][0].copy_text())
            else:
                self.descriptors[i + 1][2] = point.x()
                self.descriptors[i + 1][1] = self.descriptors[i][1]
                self.set_descriptor_pos(i + 1)

                self.descriptors[i][3] = point.x()
                self.set_descriptor_pos(i)
                return i
        raise RuntimeError("DOWNWARDS FINISH WITHOUT RETURNING")

    def update_upwards(self, index, point: QPointF):
        for i in range(index, -1, -1):
            if point.y() < self.descriptors[i][1]:

                self.descriptors[i + 1][1] = self.descriptors[i][1]
                self.descriptors[i + 1][2] = self.descriptors[i][2]
                self.set_descriptor_pos(i + 1)

                self.descriptors[i][3] = self.descriptors[i - 1][3]
                self.descriptors[i][0].paste_text(self.descriptors[i + 1][0].copy_text())
            else:
                self.descriptors[i + 1][1] = self.descriptors[i][1]
                self.descriptors[i + 1][2] = point.x()
                self.set_descriptor_pos(i + 1)

                self.descriptors[i][3] = point.x()
                self.set_descriptor_pos(i)
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

                self.descriptors[ind][1] = self.descriptors[ind - 1][1]
                self.descriptors[ind][2] = self.descriptors[ind - 1][3]
                self.descriptors[ind][3] = self.descriptors[ind - 1][3]
                self.set_descriptor_pos(ind)

                self.separators[sep_index][1] -= 1

                # Update text for this group of descriptors
                self.descriptors[ind + 1][0].emit_text_changed(False)

    def text_changed(self, changed_descriptor: Descriptor, text_changed: bool):
        # Find changed descriptor using exponential search
        desc_index = exponentialSearchDescriptors(self.descriptors, changed_descriptor.pos())

        # Find separator before the group of descriptors using exponential search
        sep_index = -1
        if len(self.separators) != 0:
            sep_index = exponentialSearchSeparators(self.separators, desc_index)

        # Adapt bounds
        if sep_index == -1:
            start = 0
        else:
            start = self.separators[sep_index][1] + 1

        if sep_index == len(self.separators) - 1:
            end = len(self.descriptors)
        else:
            end = self.separators[sep_index + 1][1] + 1

        # Update text for the rest of the descriptors of the same group
        for i in range(start, end):
            self.descriptors[i][0].paste_text(self.descriptors[desc_index][0].copy_text())

        # Emit text changed signal
        if text_changed:
            self.emitter.editable_text_changed.emit(sep_index, self.descriptors[desc_index][0].editable_text_list)

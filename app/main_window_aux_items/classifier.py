import numpy as np
from PyQt5.QtCore import Qt

from app.main_window_aux_items.rounded_rect.rounded_rect_handler import RoundedRectHandler
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsItem

from .descriptor.descriptor import TEXT_SEPARATOR, ALLOWED_STRINGS
from .descriptor.descriptor_handler import DescriptorHandler
from .main_text import MainText
from .separator.separator_handler import SeparatorHandler


def create_colors_dict(default_text: str, color_list: list[str]) -> dict[str, str]:
    """
    Create a dictionary from a list of colors. This dictionary will have as a key of each element the color
    itself and as a value, a list containing the values of the different editable parts of the descriptor text.
    :param default_text: The text that is placed in the descriptors as default.
    :param color_list: The list with the colors.
    :return: The dictionary.
    """
    editable_texts_number = len(default_text.split(TEXT_SEPARATOR)) - 1
    allo_str_len = len(ALLOWED_STRINGS)

    if len(color_list) != np.power(allo_str_len, editable_texts_number) + 1:
        raise RuntimeError("There should be " + str(np.power(allo_str_len, editable_texts_number) + 1) +
                           " colors for classifier module but got " + str(len(color_list)) + " instead.")

    colors = {"": color_list[0]}

    for i in range(1, len(color_list)):
        value = ""
        for e in range(editable_texts_number):
            if e == editable_texts_number - 1:
                value += (str(e) + ALLOWED_STRINGS[(i - 1) % allo_str_len])
            else:
                value += (str(e) + ALLOWED_STRINGS[
                    np.floor_divide(i - 1, allo_str_len * (editable_texts_number - 1 - e)) % allo_str_len
                    ])
        colors[value] = color_list[i]
    return colors


def obtain_limit_points(points):
    return [(line[0], (line[1][0], line[1][-1])) for line in points]


class Classifier:
    """
    This class controls all the behaviour of the QGraphicsItems associated with the graphical text
    classification. That is, the rectangles and its descriptors_handler and the separators between them.
    """

    def __init__(self, text: str, text_width: float, text_size: float, default_descriptor: str,
                 rect_colors: list[str], parent: QGraphicsItem) -> None:
        """
        Create TextClassifier object. Only one object form this class should be created
        :param text_width: The maximum width of this element. Is determined by the max text width.
        :param text_size: The height that the rectangles and the separators will have. Should be
                            greater than text height.
        :param parent: The QGraphicsItem parent of this element. Can't be None
        """
        self.text = MainText(text, text_size, text_width, 300, parent)

        self.fixed_points = self.text.get_points()

        # Set separators
        self.sep_handler = SeparatorHandler(text_size * 2, self.fixed_points, parent)
        self.sep_handler.add_separator(self.fixed_points[0][1][0], self.fixed_points[0][0], True)
        self.sep_handler.add_separator(self.fixed_points[-1][1][-1], self.fixed_points[-1][0], True)

        # Set separator width according to text size
        custom_pen = QPen(Qt.black)
        custom_pen.setWidth(max(1, int(text_size / 2.5)))
        self.sep_handler.set_separator_pen(custom_pen)

        self.rects_handler = RoundedRectHandler(
            text_size * 2,
            text_size / 2,
            obtain_limit_points(self.fixed_points),
            create_colors_dict(default_descriptor, rect_colors),
            parent
        )
        self.rects_handler.add_separator_listeners(
            self.sep_handler.emitter.pos_changed,
            self.sep_handler.emitter.clicked_on_the_border,
            self.sep_handler.emitter.removed
        )

        self.descriptors_handler = DescriptorHandler(
            text_size * 2.4, default_descriptor, text_size * 2 / 3, obtain_limit_points(self.fixed_points), parent
        )
        self.descriptors_handler.add_separator_listeners(
            self.sep_handler.emitter.pos_changed,
            self.sep_handler.emitter.clicked_on_the_border,
            self.sep_handler.emitter.removed
        )

        self.rects_handler.add_descriptor_listeners(self.descriptors_handler.emitter.editable_text_changed)

    def set_colors(self, colors: list[str]) -> None:
        """
        Set the colors that will be used by the rounded rects depending on the value of the descriptor. The length
        of this list should be the same as the possible combinations of the descriptor text plus one (the default one).
        Also, the colors list should be of any HTML valid color.
        :param colors: List of all available colors
        """
        self.rects_handler.set_colors(create_colors_dict(self.descriptors_handler.default_text, colors))

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
        self.descriptors_handler.set_default_text(default_descriptor)
        self.rects_handler.set_colors(create_colors_dict(self.descriptors_handler.default_text, colors))

    def get_default_descriptor(self) -> str:
        """
        Returns the default descriptor text used in all the descriptors.
        :return: The default descriptor as a string
        """
        return self.descriptors_handler.default_text

    def split(self, x: float, y: float) -> bool:
        """
        Splits the nearest rectangle to the given coordinates in two, placing a separator where
        the split has been made.
        :param x: The x coordinate
        :param y: The y coordinate
        :return: True if success, False if error. There can be a mistake if the coordinates
                 are out of bounds or if there is no more space to place a separator
        """
        return self.sep_handler.add_separator(x, y, False)

    def join(self, x: float, y: float) -> bool:
        """
        Remove a separator and join the two remaining rectangles.
        :param x: The x coordinate
        :param y: The y coordinate
        :return: True if success, False if error. There can be a mistake if the coordinates
                 are out of bounds or if in the given coordinates there is no separator
        """
        removed_separator = self.sep_handler.delete_separator(x, y)

        if removed_separator is None:
            return False

        return True

    def get_text_classified(self) -> list[str]:
        """
        Gets the subgroups of words that form the separators within the text.
        :return: A list with a group of words per element.
        """
        text_list = [""] * (len(self.sep_handler.separators) - 1)
        separator_points = self.sep_handler.get_separator_points()

        # This ind will be used to access all the positions in separator_points
        separator_index = 0

        complete_point_list = self.text.get_complete_points()

        for y_index in range(len(complete_point_list)):
            for x_index in range(len(complete_point_list[y_index][1])):
                if separator_points[separator_index].x() == complete_point_list[y_index][1][x_index][0] and \
                        separator_points[separator_index].y() == complete_point_list[y_index][0]:
                    separator_index += 1
                if complete_point_list[y_index][1][x_index][1] != '':
                    text_list[separator_index - 1] += (complete_point_list[y_index][1][x_index][1] + " ")

        # Remove last space in every item and empty items
        popped_elements = 0
        for i in range(len(text_list)):
            if text_list[i - popped_elements] == "":
                text_list.pop(i - popped_elements)
                popped_elements += 1
            else:
                text_list[i - popped_elements] = text_list[i - popped_elements][:-1]
        return text_list

    def get_text_analyzed(self) -> list[tuple[str, str]]:
        """
        Gets the subgroups of words that form the separators within the text and its descriptor tag.
        :return: A list of tuples with the text classified and analyzed. The first tuple element is the text and the
                 second is the descriptor value.
        """
        analyzed_text = []
        text_list = self.get_text_classified()
        descriptors_list = self.descriptors_handler.get_descriptor_values()

        for i in range(len(descriptors_list)):
            analyzed_text.append((text_list[i], descriptors_list[i]))
        return analyzed_text
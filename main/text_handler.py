from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QFont, QPen, QPainter
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsLineItem

from text_classifier import TextClassifier
from custom_text import CustomText


class TextHandler(QGraphicsView):
    """
    This class controls all the behaviour of the QGraphicsItems associated with the graphical text
    classification. That is, the rectangles and its descriptors and the separators between them.
    """

    def __init__(self, x_padding, y_padding, min_width, min_height, text, text_size, colors):
        super().__init__()
        self.scene = QGraphicsScene(0, 0, min_width, min_height)

        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.setMinimumSize(min_width, min_height)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.items_parent = QGraphicsLineItem()
        self.items_parent.setPos(x_padding, y_padding)
        self.items_parent.setOpacity(0)
        self.scene.addItem(self.items_parent)

        self.font = QFont()
        self.font.setFamily('Times')
        self.font.setBold(True)

        self.text = CustomText(text, min_width - 2 * x_padding, 300, self.items_parent)

        self.classifier = TextClassifier(
            min_width - 2 * x_padding, text_size * 2, self.text.get_points(), "SD~;SG~", colors, self.items_parent
        )

        self.set_text_size(text_size)

        custom_pen = QPen(Qt.black)
        custom_pen.setWidth(5)
        self.set_separator_style(custom_pen)

    def set_separator_style(self, pen: QPen) -> None:
        """
        Set pen for all the separators and adjust multiline rects offset to the pen width
        :param pen: The pen.
        """
        self.classifier.set_separator_pen(pen)
        self.classifier.set_multiline_rects_offset(pen.widthF() / 4)

    def split(self, x_value, y_value):
        """
        Splits the nearest rectangle to the given coordinates in two, placing a separator where
        the split has been made.
        :param x_value: The x coordinate
        :param y_value: The y coordinate
        :return: True if success, False if error. There can be a mistake if the coordinates
                 are out of bounds or if there is no more space to place a separator
        """
        return self.classifier.split(x_value, y_value)

    def join(self, x_value, y_value):
        """
        Remove a separator and join the two remaining rectangles.
        :param x_value: The x coordinate
        :param y_value: The y coordinate
        :return: True if success, False if error. There can be a mistake if the coordinates
                 are out of bounds or if in the given coordinates there is no separator
        """
        return self.classifier.join(x_value, y_value)

    def set_text(self, text: str) -> None:
        """
        Set the text to be analyzed.
        :param text: The text that will appear.
        """
        self.text.set_text(text)
        self.classifier.reset(self.text.get_points())

    def set_text_size(self, text_size):
        # Save text_list from the original text_size to reposition all the separators
        text_list_previous_size = self.get_text_classified()

        # Set text size
        self.font.setPointSize(text_size)
        self.text.setFont(self.font)
        self.scene.setSceneRect(
            0,
            0,
            self.size().width(),
            self.items_parent.pos().y() + self.text.boundingRect().height()
        )

        # Change rects and separators height
        self.classifier.set_line_height(text_size * 2)

        # Reposition separators to the new text size
        self.set_separators_reposition(text_list_previous_size)

    def get_text_classified(self):
        text_list = [""] * (len(self.classifier.separators) - 1)
        separator_points = self.classifier.get_separator_points()

        # This index will be used to access all the positions in separator_points
        separator_index = 0

        for y_index in range(len(self.text.point_list)):
            for x_index in range(len(self.text.point_list[y_index][1])):
                if separator_points[separator_index].x() == self.text.point_list[y_index][1][x_index][0] and \
                        separator_points[separator_index].y() == self.text.point_list[y_index][0]:
                    separator_index += 1
                if self.text.point_list[y_index][1][x_index][1] != '':
                    text_list[separator_index - 1] += (self.text.point_list[y_index][1][x_index][1] + " ")

        # Remove last space in every item and empty items
        popped_elements = 0
        for i in range(len(text_list)):
            if text_list[i - popped_elements] == "":
                text_list.pop(i - popped_elements)
                popped_elements += 1
            else:
                text_list[i - popped_elements] = text_list[i - popped_elements][:-1]
        return text_list

    def set_separators_reposition(self, text_list):
        text_list_index = 0
        separator_points = [QPointF(self.text.point_list[0][1][0][0], self.text.point_list[0][0])]
        aux_text = ""

        for y_index in range(len(self.text.point_list)):
            for x_index in range(len(self.text.point_list[y_index][1])):
                if self.text.point_list[y_index][1][x_index][1] != '':
                    aux_text += (self.text.point_list[y_index][1][x_index][1] + " ")

                    # Do the comparison without the last space character
                    if aux_text[:-1] not in text_list[text_list_index]:
                        text_list_index += 1
                        aux_text = self.text.point_list[y_index][1][x_index][1] + " "
                        separator_points.append(
                            QPointF(self.text.point_list[y_index][1][x_index][0], self.text.point_list[y_index][0])
                        )
        # Add last element
        separator_points.append(
            QPointF(self.text.point_list[-1][1][-1][0], self.text.point_list[-1][0])
        )

        self.classifier.update_general_fixed_points_and_separators_pos(self.text.get_points(), separator_points)

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
        self.classifier.set_default_descriptor(default_descriptor, colors)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        """
        This function allows to resize the QGraphicsView item and the scene in it.
        :param event: The ResizeEvent object.
        """
        super().resizeEvent(event)
        if event.size().width() != event.oldSize().width():
            # Save text_list from the original text_size to reposition all the separators
            text_list_previous_size = self.get_text_classified()

            real_width = event.size().width() - 2 * self.items_parent.pos().x()

            # Set text width
            self.text.set_width(real_width)

            self.scene.setSceneRect(
                0,
                0,
                self.size().width(),
                self.items_parent.pos().y() + self.text.boundingRect().height()
            )

            # Reposition separators to the new text size
            self.set_separators_reposition(text_list_previous_size)

            self.classifier.set_width(real_width)
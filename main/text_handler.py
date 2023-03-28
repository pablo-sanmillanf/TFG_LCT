from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QFont, QPen, QPainter
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsLineItem

from text_classifier import TextClassifier
from custom_text import CustomText


COLORS = [
            "lavender",
            "gold",
            "goldenrod",
            "yellow",
            "orange",
            "red",
            "sienna",
            "firebrick",
            "deeppink",
            "magenta",
            "orangered",
            "brown",
            "yellowgreen",
            "chocolate",
            "coral",
            "papayawhip",
            "bisque",
        ]


class TextHandler(QGraphicsView):
    """
    This class controls all the behaviour of the QGraphicsItems associated with the graphical text
    classification. That is, the rectangles and its descriptors and the separators between them.
    """

    def __init__(self, x_padding, y_padding, width, height, text, text_size):
        super().__init__()

        self.scene = QGraphicsScene(0, 0, width + 2 * x_padding, height)

        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.setFixedSize(width + 2 * x_padding, height)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.items_parent = QGraphicsLineItem()
        self.items_parent.setPos(x_padding, y_padding)
        self.items_parent.setOpacity(0)
        self.scene.addItem(self.items_parent)

        self.font = QFont()
        self.font.setFamily('Times')
        self.font.setBold(True)

        self.text = CustomText(text, width, 300, self.items_parent)

        self.classifier = TextClassifier(
            width, text_size * 2, self.text.get_points(), "SD~;SG~", COLORS, self.items_parent
        )

        self.change_text_size(text_size)

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
        return self.classifier.split(x_value, y_value)

    def join(self, x_value, y_value):
        return self.classifier.join(x_value, y_value)

    def change_text_size(self, text_size):
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

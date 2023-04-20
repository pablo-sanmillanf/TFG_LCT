from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsLineItem, QWidget, QMenu, QAction

from main_window_aux_items.classifier import Classifier


def format_text(text: str) -> str:
    """
    This function format the text to adapt it to the required format by classes TextClassifier and MainText.
    More specifically, replace the "\n" with "<br>" and remove duplicate spaces.
    :param text: The text to be formatted.
    :return: The formatted text.
    """
    text = text.replace("&", "&amp;")
    text = text.replace("\"", "&quot;")
    text = text.replace(">", "&gt;")
    text = text.replace("<", "&lt;")
    return " ".join(text.replace("\n", " <br> ").split())


class ClassifierView(QGraphicsView):
    """
    This class controls all the behaviour of the QGraphicsItems, the QGraphicsView and the QGraphicsScene.
    """
    split_action: QAction
    join_action: QAction
    classifier: Classifier

    def __init__(self, parent: QWidget) -> None:
        """
        Create TextHandler object. Only one object form this class should be created.
        :param parent: The QWidget parent object.
        """
        super().__init__(parent)
        self.scene = None
        self.items_parent = None
        self.font = None
        self.context_menu_pos = None
        self.global_pos_y_offset = None

    def setup(self, x_padding: float | int, y_padding: float | int, min_width: float | int, min_height: float | int,
              text: str, text_size: float | int, default_descriptor: str, colors: list[str]) -> None:
        """
        Set up the object.
        :param x_padding: Pixels of horizontal padding for the text.
        :param y_padding: Pixels of vertical padding for the text.
        :param min_width: Minimum width of the item.
        :param min_height: Minimum height of the item.
        :param text: The text to analyze. New lines in this text should be represented as '\n' characters.
        :param text_size: The text size as a number. All the elements in QGraphicsScene will adjust their size to
                          the text size.
        :param default_descriptor: The text that will appear in the descriptor as default. Depending on the number of
                                   "~" characters, the length of the colors' parameter will change.
        :param colors: A list of colors that will be used by the rectangles as a background color depending on the
                       values of its Descriptors. Should be valid HTML colors.
        """
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

        self.classifier = Classifier(
            format_text(text),
            min_width - 2 * x_padding,
            text_size,
            default_descriptor,
            colors,
            self.items_parent
        )

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu)

        self.split_action = QAction("Split", self)
        self.join_action = QAction("Join", self)
        self.split_action.setStatusTip("Split clause in two")
        self.join_action.setStatusTip("Join the two clauses in one")
        self.split_action.triggered.connect(self.split)
        self.join_action.triggered.connect(self.join)

        # As the rectangles height is 2*text_size this offset moves the point to calculate half height.
        self.global_pos_y_offset = -text_size

    def on_context_menu(self, pos: QPoint) -> None:
        """
        This function set a context menu
        :param pos: The clicked position as a QPoint.
        """

        self.context_menu_pos = pos
        self.join_action.setEnabled(
            self.classifier.there_is_a_separator(
                pos.x() - self.items_parent.pos().x(),
                pos.y() - self.items_parent.pos().y() + self.global_pos_y_offset + self.verticalScrollBar().value()
            )
        )

        context = QMenu(self)
        context.addAction(self.split_action)
        context.addAction(self.join_action)
        context.exec(self.mapToGlobal(pos))

    def get_text_size(self) -> int | float:
        """
        Return the text size.
        :return: The text size as a number.
        """
        return self.classifier.get_text_size()

    def split(self) -> None:
        """
        Splits the nearest rectangle to the self.context_menu_pos in two, placing a separator where
        the split has been made.
        """
        self.classifier.split(
            self.context_menu_pos.x() - self.items_parent.pos().x(),
            self.context_menu_pos.y() - self.items_parent.pos().y() +
            self.global_pos_y_offset + self.verticalScrollBar().value()
        )

    def join(self) -> None:
        """
        Remove a separator and join the two remaining rectangles.
        """
        self.classifier.join(
            self.context_menu_pos.x() - self.items_parent.pos().x(),
            self.context_menu_pos.y() - self.items_parent.pos().y() +
            self.global_pos_y_offset + self.verticalScrollBar().value()
        )

    def set_text(self, text: str) -> None:
        """
        Set the text to be analyzed.
        :param text: The text that will appear.
        """
        self.classifier.set_text(format_text(text))

        # Set text size
        self.scene.setSceneRect(
            0,
            0,
            self.size().width(),
            self.items_parent.pos().y() + self.classifier.get_text_item_height()
        )

    def set_text_size(self, text_size: float | int) -> None:
        """
        Set the text size. Also, the height of the separators and the rects and the text size of the descriptors is
        changed.
        :param text_size: The text size as a number.
        """
        self.global_pos_y_offset = -text_size

        self.classifier.set_text_size(text_size)

        self.scene.setSceneRect(
            0,
            0,
            self.size().width(),
            self.items_parent.pos().y() + self.classifier.get_text_item_height()
        )

    def get_text_analyzed(self) -> list[tuple[str, str]]:
        """
        Gets the subgroups of words that form the separators within the text and its descriptor tag.
        :return: A list of tuples with the text classified and analyzed. The first tuple element is the text and the
                 second is the descriptor value.
        """
        return self.classifier.get_text_analyzed()

    def get_text_classified(self) -> list[str]:
        """
        Gets the subgroups of words that form the separators within the text.
        :return: A list with a group of words per element.
        """
        return self.classifier.get_text_classified()

    def get_default_descriptor(self) -> str:
        """
        Returns the default descriptor used in all the descriptors_handler.
        :return: The default descriptor as a string
        """
        return self.classifier.get_default_descriptor()

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

    def set_colors(self, colors: list[str]) -> None:
        """
        Set the colors that will be used by the rounded rects depending on the value of the descriptor. The length
        of this list should be the same as the possible combinations of the descriptor text plus one (the default one).
        Also, the colors list should be of any HTML valid color.
        :param colors: List of all available colors
        """
        self.classifier.set_colors(colors)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        """
        This function allows to resize the QGraphicsView item and the scene in it.
        :param event: The ResizeEvent object.
        """
        super().resizeEvent(event)
        if event.size().width() != event.oldSize().width():
            real_width = event.size().width() - 2 * self.items_parent.pos().x()

            # Set text width
            self.classifier.set_width(real_width)

            self.scene.setSceneRect(
                0,
                0,
                self.size().width(),
                self.items_parent.pos().y() + self.classifier.get_text_item_height()
            )

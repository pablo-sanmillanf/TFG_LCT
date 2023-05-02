from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QPoint, QTimerEvent
from PyQt5.QtGui import QPainter, QCursor
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsLineItem, QWidget, QMenu, QAction, QApplication

from main_window_aux_items.classifier import Classifier


class ClassifierView(QGraphicsView):
    """
    This class controls all the behaviour of the QGraphicsItems, the QGraphicsView and the QGraphicsScene.
    """
    promote_separator_action: QAction
    demote_separator_action: QAction
    split_action: QAction
    join_action: QAction
    classifier: Classifier

    def __init__(self, parent: QWidget) -> None:
        """
        Create TextHandler object. Only one object form this class should be created.
        :param parent: The QWidget parent object.
        """
        super().__init__(parent)
        self.timerId = 0
        self.real_width = 0
        self.scene = None
        self.items_parent = None
        self.font = None
        self.context_menu_pos = None
        self.global_pos_y_offset = None

    def setup(self, x_padding: float | int, y_padding: float | int, min_width: float | int, min_height: float | int,
              text: str, text_size: float | int, default_descriptor: str, default_descriptor_value: str,
              allowed_descriptor_values: list[str], colors: list[str]) -> None:
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
            text,
            min_width - 2 * x_padding,
            text_size,
            default_descriptor,
            default_descriptor_value,
            allowed_descriptor_values,
            colors,
            self.items_parent
        )

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._on_context_menu)

        self.split_action = QAction("Split", self)
        self.join_action = QAction("Join", self)
        self.promote_separator_action = QAction("Promote to super separator", self)
        self.demote_separator_action = QAction("Demote from super separator", self)
        self.split_action.setStatusTip("Split clause in two")
        self.join_action.setStatusTip("Join the two clauses in one")
        self.split_action.triggered.connect(self.split)
        self.join_action.triggered.connect(self.join)
        self.promote_separator_action.triggered.connect(self.promote_separator)
        self.demote_separator_action.triggered.connect(self.demote_separator)

        # As the rectangles height is 2*text_size this offset moves the point to calculate half height.
        self.global_pos_y_offset = -text_size

    def _on_context_menu(self, pos: QPoint) -> None:
        """
        This function set a context menu
        :param pos: The clicked position as a QPoint.
        """

        self.context_menu_pos = pos

        there_is_a_separator = self.classifier.there_is_a_separator(
                pos.x() - self.items_parent.pos().x(),
                pos.y() - self.items_parent.pos().y() + self.global_pos_y_offset + self.verticalScrollBar().value()
            )

        is_super_separator = self.classifier.is_super_separator(
                pos.x() - self.items_parent.pos().x(),
                pos.y() - self.items_parent.pos().y() + self.global_pos_y_offset + self.verticalScrollBar().value()
            )

        self.join_action.setEnabled(there_is_a_separator)

        self.promote_separator_action.setEnabled(there_is_a_separator and not is_super_separator)

        self.demote_separator_action.setEnabled(there_is_a_separator and is_super_separator)

        context = QMenu(self)
        context.addAction(self.split_action)
        context.addAction(self.join_action)
        context.addAction(self.promote_separator_action)
        context.addAction(self.demote_separator_action)
        context.exec(self.mapToGlobal(pos))

    def get_text(self) -> str:
        return self.classifier.get_text()

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
        """while self.classifier.split(0,0):
            pass"""

    def join(self) -> None:
        """
        Remove a separator and join the two remaining rectangles.
        """
        self.classifier.join(
            self.context_menu_pos.x() - self.items_parent.pos().x(),
            self.context_menu_pos.y() - self.items_parent.pos().y() +
            self.global_pos_y_offset + self.verticalScrollBar().value()
        )

    def promote_separator(self) -> None:
        """
        Remove a separator and join the two remaining rectangles.
        """
        self.classifier.promote_separator(
            self.context_menu_pos.x() - self.items_parent.pos().x(),
            self.context_menu_pos.y() - self.items_parent.pos().y() +
            self.global_pos_y_offset + self.verticalScrollBar().value()
        )

    def demote_separator(self) -> None:
        """
        Remove a separator and join the two remaining rectangles.
        """
        self.classifier.demote_separator(
            self.context_menu_pos.x() - self.items_parent.pos().x(),
            self.context_menu_pos.y() - self.items_parent.pos().y() +
            self.global_pos_y_offset + self.verticalScrollBar().value()
        )

    def set_text(self, text: str) -> None:
        """
        Set the text to be analyzed.
        :param text: The text that will appear.
        """
        self.classifier.set_text(text)

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

        app = QApplication.instance()

        app.setOverrideCursor(QCursor(Qt.WaitCursor))

        self.global_pos_y_offset = -text_size

        self.classifier.set_text_size(text_size)

        self.scene.setSceneRect(
            0,
            0,
            self.size().width(),
            self.items_parent.pos().y() + self.classifier.get_text_item_height()
        )

        app.restoreOverrideCursor()

    def set_text_analyzed(self, sep_text_list: list[str], super_sep_text_list: list[str], default_descriptor: [str],
                          colors: list[str], labels: list[str], values: list[list[str]]):
        self.classifier.set_text_analyzed(
            sep_text_list,
            super_sep_text_list,
            default_descriptor,
            colors,
            labels,
            values
        )

    def get_text_analyzed(self) -> list[tuple[list[tuple[str, str]], str]]:
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
            self.real_width = event.size().width() - 2 * self.items_parent.pos().x()
            if self.timerId:
                self.killTimer(self.timerId)
                self.timerId = 0

            self.timerId = self.startTimer(500)

    def timerEvent(self, a0: 'QTimerEvent') -> None:
        self.killTimer(self.timerId)
        self.timerId = 0

        app = QApplication.instance()

        app.setOverrideCursor(QCursor(Qt.WaitCursor))

        # Set text width
        self.classifier.set_width(self.real_width)

        self.scene.setSceneRect(
            0,
            0,
            self.size().width(),
            self.items_parent.pos().y() + self.classifier.get_text_item_height()
        )

        app.restoreOverrideCursor()

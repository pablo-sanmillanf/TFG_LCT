from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QPoint, QTimerEvent, QSemaphore
from PyQt5.QtGui import QPainter, QCursor
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsLineItem, QWidget, QMenu, QAction, QApplication

from .main_window_aux_items.classifier import Classifier


class ClassifierView(QGraphicsView):
    """
    This class controls all the behaviour of the QGraphicsItems, the QGraphicsView and the QGraphicsScene.
    """
    _time = 1
    _promote_separator_action: QAction
    _demote_separator_action: QAction
    _split_action: QAction
    _join_action: QAction
    classifier: Classifier

    def __init__(self, parent: QWidget) -> None:
        """
        Create ClassifierView object. Only one object form this class should be created.
        :param parent: The QWidget parent object.
        """
        super().__init__(parent)
        self._timerId = 0
        self._real_width = 0
        self._scene = None
        self._items_parent = None
        self._context_menu_pos = None
        self._global_pos_y_offset = None
        self._semaphore = QSemaphore()

    def setup(self, x_padding: float | int, y_padding: float | int, min_width: float | int, min_height: float | int,
              text: str, text_size: float | int, default_descriptor: str, default_descriptor_value: str,
              allowed_descriptor_values: list[str], colors: list[str], regular_sep_color: str,
              super_sep_color: str) -> None:
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
                                   "default_descriptor_value" characters, the length of the colors' parameter will
                                   change.
        :param default_descriptor_value: The default value of editable parts of the descriptors.
        :param allowed_descriptor_values: The allowed values that can be the editable parts of the descriptors.
        :param colors: A list of colors that will be used by the rectangles as a background color depending on the
                       values of its Descriptors. Should be valid HTML colors.
        :param regular_sep_color: A valid HTML color that will have the regular separators.
        :param super_sep_color: A valid HTML color that will have the super separators.
        """
        self._scene = QGraphicsScene(0, 0, min_width, min_height)

        self.setScene(self._scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.setMinimumSize(min_width, min_height)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self._items_parent = QGraphicsLineItem()
        self._items_parent.setPos(x_padding, y_padding)
        self._items_parent.setOpacity(0)
        self._scene.addItem(self._items_parent)

        self.classifier = Classifier(
            text,
            min_width - 2 * x_padding,
            text_size,
            default_descriptor,
            default_descriptor_value,
            allowed_descriptor_values,
            colors,
            regular_sep_color,
            super_sep_color,
            self._items_parent
        )

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._on_context_menu)

        self._split_action = QAction("Split", self)
        self._join_action = QAction("Join", self)
        self._promote_separator_action = QAction("Promote to super separator", self)
        self._demote_separator_action = QAction("Demote from super separator", self)
        self._split_action.setStatusTip("Split clause in two")
        self._join_action.setStatusTip("Join the two clauses in one")
        self._split_action.triggered.connect(self._split)
        self._join_action.triggered.connect(self._join)
        self._promote_separator_action.triggered.connect(self._promote_separator)
        self._demote_separator_action.triggered.connect(self._demote_separator)

        # As the rectangles height is 2*text_size this offset moves the point to calculate half height.
        self._global_pos_y_offset = -text_size

    def _on_context_menu(self, pos: QPoint) -> None:
        """
        This function sets-up a context menu
        :param pos: The clicked position as a QPoint.
        """

        self._context_menu_pos = pos

        there_is_a_separator = self.classifier.there_is_a_separator(
            pos.x() - self._items_parent.pos().x(),
            pos.y() - self._items_parent.pos().y() + self._global_pos_y_offset + self.verticalScrollBar().value()
            )

        is_super_separator = self.classifier.is_super_separator(
            pos.x() - self._items_parent.pos().x(),
            pos.y() - self._items_parent.pos().y() + self._global_pos_y_offset + self.verticalScrollBar().value()
            )

        self._join_action.setEnabled(there_is_a_separator)

        self._promote_separator_action.setEnabled(there_is_a_separator and not is_super_separator)

        self._demote_separator_action.setEnabled(there_is_a_separator and is_super_separator)

        context = QMenu(self)
        context.addAction(self._split_action)
        context.addAction(self._join_action)
        context.addAction(self._promote_separator_action)
        context.addAction(self._demote_separator_action)
        context.exec(self.mapToGlobal(pos))

    def get_text(self) -> str:
        """
        Obtain the plain text that is being analyzed.
        :return: The plain text.
        """
        return self.classifier.get_text()

    def get_text_size(self) -> int | float:
        """
        Return the text size.
        :return: The text size as a number.
        """
        return self.classifier.get_text_size()

    def _split(self) -> None:
        """
        Splits the nearest rectangle to the self._context_menu_pos in two, placing a separator where
        the split has been made.
        """
        self.classifier.split(
            self._context_menu_pos.x() - self._items_parent.pos().x(),
            self._context_menu_pos.y() - self._items_parent.pos().y() +
            self._global_pos_y_offset + self.verticalScrollBar().value()
        )

    def _join(self) -> None:
        """
        Remove a separator and join the two remaining rectangles.
        """
        self.classifier.join(
            self._context_menu_pos.x() - self._items_parent.pos().x(),
            self._context_menu_pos.y() - self._items_parent.pos().y() +
            self._global_pos_y_offset + self.verticalScrollBar().value()
        )

    def _promote_separator(self) -> None:
        """
        Promote the Separator in the self._context_menu_pos position to a super Separator. If there is no Separator in
        this position, this function will do nothing.
        """
        self.classifier.promote_separator(
            self._context_menu_pos.x() - self._items_parent.pos().x(),
            self._context_menu_pos.y() - self._items_parent.pos().y() +
            self._global_pos_y_offset + self.verticalScrollBar().value()
        )

    def _demote_separator(self) -> None:
        """
        Demote a super Separator in the self._context_menu_pos position to a regular Separator. If there is no Separator
        in this position, this function will do nothing.
        """
        self.classifier.demote_separator(
            self._context_menu_pos.x() - self._items_parent.pos().x(),
            self._context_menu_pos.y() - self._items_parent.pos().y() +
            self._global_pos_y_offset + self.verticalScrollBar().value()
        )

    def set_text(self, text: str) -> None:
        """
        Set the text to be analyzed.
        :param text: The text that will appear.
        """
        app = QApplication.instance()

        app.setOverrideCursor(QCursor(Qt.WaitCursor))

        if not self.verticalScrollBar().isVisible():
            self._time = 0
            self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

            self._semaphore.acquire()

        self.classifier.set_text(text)

        # Set text size
        self._scene.setSceneRect(
            0,
            0,
            self.size().width(),
            self._items_parent.pos().y() + self.classifier.get_text_item_height()
        )
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self._time = 500
        app.restoreOverrideCursor()

    def set_text_size(self, text_size: float | int) -> None:
        """
        Set the text size. Also, the height of the separators and the rects and the text size of the descriptors is
        changed to maintain the proportion.
        :param text_size: The text size as a number.
        """

        app = QApplication.instance()

        app.setOverrideCursor(QCursor(Qt.WaitCursor))

        self._global_pos_y_offset = -text_size

        self.classifier.set_text_size(text_size)

        self._scene.setSceneRect(
            0,
            0,
            self.size().width(),
            self._items_parent.pos().y() + self.classifier.get_text_item_height()
        )

        app.restoreOverrideCursor()

    def set_text_analyzed(self, sep_text_list: list[str], super_sep_text_list: list[str], default_descriptor: [str],
                          colors: list[str], labels: list[str], values: list[list[str]]):
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
        app = QApplication.instance()

        app.setOverrideCursor(QCursor(Qt.WaitCursor))

        if not self.verticalScrollBar().isVisible():
            self._time = 0
            self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

            self._semaphore.acquire()

        # Set text width
        self.classifier.set_text_analyzed(
            sep_text_list,
            super_sep_text_list,
            default_descriptor,
            colors,
            labels,
            values
        )

        self._scene.setSceneRect(
            0,
            0,
            self.size().width(),
            self._items_parent.pos().y() + self.classifier.get_text_item_height()
        )
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self._time = 500
        app.restoreOverrideCursor()

    def get_text_analyzed(self) -> list[tuple[list[tuple[str, str]], str]]:
        """
        Gets the subgroups of words that form the separators within the text and its descriptor tag. Also, obtain the
        tag for all the super separator groups.
        :return: A list of tuples with the text classified and analyzed. The first tuple element is a list with all the
        clauses between two super Separators analyzed and the second element of the tuple is the descriptor value of
        this super clause.
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
        Returns the default descriptor used in all the descriptors.
        :return: The default descriptor as a string
        """
        return self.classifier.get_default_descriptor()

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
        This function allows to resize the QGraphicsView item. After 0.5 seconds, also the scene in it and all the
        graphics items will be resized. This behaviour has set to avoid calculate all the new position for the graphics
        items every time the user resizes a pixel the window, resulting in a smoother performance.
        :param event: The QResizeEvent object.
        """
        super().resizeEvent(event)
        if event.size().width() != event.oldSize().width():
            self._real_width = event.size().width() - 2 * self._items_parent.pos().x()
            if self._timerId:
                self.killTimer(self._timerId)
                self._timerId = 0

            if self._time == 0:
                self.classifier.set_width(self._real_width)
                if self._semaphore.available() == 0:
                    self._semaphore.release()
            else:
                self._timerId = self.startTimer(self._time)

    def timerEvent(self, a0: 'QTimerEvent') -> None:
        """
        This function is triggered 0.5 seconds after the resizing of the window and set the reposition for the
        QGraphicsScene and all the QGraphicsItem of the classifier object.
        :param a0: The QTimerEvent object. Non-relevant.
        """
        self.killTimer(self._timerId)
        self._timerId = 0

        app = QApplication.instance()

        app.setOverrideCursor(QCursor(Qt.WaitCursor))

        # Set text width
        self.classifier.set_width(self._real_width)

        self._scene.setSceneRect(
            0,
            0,
            self.size().width(),
            self._items_parent.pos().y() + self.classifier.get_text_item_height()
        )

        app.restoreOverrideCursor()

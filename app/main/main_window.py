import json

from PyQt5 import QtGui
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtWidgets import (
    QMainWindow, QInputDialog, QMessageBox, QFileDialog
)

from .text_splitter import SentenceSplitter
from .lct_handler import LCTHandler
from .dialogs.colors_dialog import ColorsDialog
from .graph.graph_window import GraphWindow
from .mainWindowQtCreator import Ui_MainWindow
from .main_resources import main_resources

SD_VALUES = ["SD--", "SD-", "SD+", "SD++"]
SG_VALUES = ["SG++", "SG+", "SG-", "SG--"]
DEFAULT_TEXT_SG = "SG~"
DEFAULT_TEXT_SD = "SD~"
DEFAULT_TEXT_SD_SG = "SD~;SG~"
DEFAULT_DESCRIPTOR_VALUE = "~"
ALLOWED_DESCRIPTOR_VALUES = ["++", "+", "-", "--"]


def manage_file(file: str, operation: str, data: str = None) -> str:
    """
    Manage the open and close of the file passed as parameter and read/write from/on it depending on the operation.
    If the operation is read ("r"), the data parameter should be None. If the operation is write ("w"), the data
    parameter is the data that will be written in the file.
    :param file: The file where read/write from/on.
    :param operation: The operation to the file. Should be "r" or "w"
    :param data: If the operation is "w", the data to write in the file. None, otherwise.
    :return: If the operation is "r", the data read from the file. None, otherwise.
    """
    result = None
    f = None
    try:
        f = open(file, operation, encoding="utf8")
        if operation == "r":
            result = f.read()
        elif operation == "w":
            f.write(data)
    finally:
        f.close()
    return result


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    This class represents the main window of the application, where the text analysis is made. Also handles the actions
    from the bar menu and trigger the plotter window.
    """
    def __init__(self, root_directory: str = "./", conf_info: str = None) -> None:
        """
        Object creator. Should be only one of those objects.
        :param root_directory: The directory set as default to find and save all the files.
        :param conf_info: A json string with all relevant information to configure the current project, such as the text
                          size, and the background colors of the RoundedRect.
        """
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(':/icon/logo'))

        self._root_directory = root_directory

        self._current_file = ""

        self._lct_handler = LCTHandler("Semantics", [SD_VALUES, SG_VALUES])

        self._graph_window = GraphWindow(root_directory + "/graph/")
        if conf_info is not None:
            try:
                self._conf = json.loads(conf_info)
            except:
                file = QFile(":/conf/defconf")
                file.open(QFile.ReadOnly)
                self._conf = json.loads(QTextStream(file.readAll()).readAll())
        else:
            file = QFile(":/conf/defconf")
            file.open(QFile.ReadOnly)
            data = QTextStream(file.readAll()).readAll()
            self._conf = json.loads(data)

        self._conf_has_changed = False
        self._not_saved = False

        self._classifierView.setup(
            10,
            10,
            500,
            500,
            "This is an example text. If you want to start editing a file select \"File\"->\"Open...\" and browse to "
            "desired file.\nTo set a division in the text, right-click and select \"Split\". To undo a division in the "
            "text, right-click and select \"Join\" near the splitter.",
            self._conf["text_size"],
            DEFAULT_TEXT_SD_SG,
            DEFAULT_DESCRIPTOR_VALUE,
            ALLOWED_DESCRIPTOR_VALUES,
            list(self._conf["colors"]["together"].values())
        )
        self._classifierView.classifier.emitter.classifier_has_changed.connect(self._classifier_has_changed)

        self._actionNew.triggered.connect(self._new_file_dialog)
        self._actionOpen.triggered.connect(self._open_file_dialog)
        self._actionSave.triggered.connect(self._save_file_dialog)
        self._actionSave_as.triggered.connect(self._save_as_file_dialog)
        self._actionText_size.triggered.connect(self._text_size_dialog)
        self._actionRects_colors.triggered.connect(self._rects_colors_dialog)
        self._actionSD.triggered.connect(lambda checked: self._target_action(DEFAULT_TEXT_SD))
        self._actionSG.triggered.connect(lambda checked: self._target_action(DEFAULT_TEXT_SG))
        self._actionSD_SG.triggered.connect(lambda checked: self._target_action(DEFAULT_TEXT_SD_SG))
        self._actiongroupTarget.setExclusive(True)
        self._actionRun_Plotter.triggered.connect(self._run_graph_window)
        self._actionSplit_in_sentences.triggered.connect(self._split_in_sentences_action)

        self.conf_data = None

        self.showMaximized()

    def _classifier_has_changed(self) -> None:
        """
        Triggered when something has changed in the classifier. Is used to know if there are unsaved changes.
        """
        self._not_saved = True

    def _new_file_dialog(self, s: bool) -> None:
        """
        Triggered when the user wants to create a new analysis from a text file. Opens a new dialog to find the desired
        text file and if it has valid content, is loaded to the classifier with the default descriptor values.
        :param s: Button state. Non-relevant.
        """
        file, file_type = QFileDialog().getOpenFileName(
            self,
            "Create new file from text file to analyze",
            self._root_directory,
            "Text files (*.txt)"
        )
        if file != "":
            text = manage_file(file, "r")
            if text is None or text == "":
                QMessageBox.critical(self, "File Error", "The selected file has not valid content", QMessageBox.Ok)
                self._new_file_dialog(True)
            else:
                self._current_file = ""
                self._classifierView.set_text(text)

    def _open_file_dialog(self, s: bool) -> None:
        """
        Triggered when the user wants to open an existing analysis from a .lct file. Opens a new dialog to find the
        desired .lct file and if it has valid content, is loaded to the classifier.
        :param s: Button state. Non-relevant.
        """
        file, file_type = QFileDialog().getOpenFileName(
            self,
            "Open file to analyze",
            self._root_directory + "/analysis",
            "LCT Files (*.lct)"
        )
        if file != "":
            text = manage_file(file, "r")
            if text is None or text == "":
                QMessageBox.critical(self, "File Error", "The selected file has not valid content", QMessageBox.Ok)
                self._open_file_dialog(True)
            else:
                if not self._lct_handler.upload_from_xml_string(text, True):
                    QMessageBox.critical(self, "File Error", "The selected file has not valid content", QMessageBox.Ok)
                    self._open_file_dialog(True)
                else:

                    raw_labels = self._lct_handler.get_raw_labels()
                    if raw_labels[0] in DEFAULT_TEXT_SG:
                        self._current_file = file

                        self._classifierView.set_text_analyzed(
                            self._lct_handler.get_clause_texts(),
                            self._lct_handler.get_super_clause_texts(),
                            DEFAULT_TEXT_SG,
                            list(self._conf["colors"]["alone"].values()),
                            raw_labels,
                            self._lct_handler.get_clause_tags()
                        )
                        self._actionSG.setChecked(True)
                        self._not_saved = False
                    elif raw_labels[0] in DEFAULT_TEXT_SD:
                        if len(raw_labels) == 1:
                            self._current_file = file

                            self._classifierView.set_text_analyzed(
                                self._lct_handler.get_clause_texts(),
                                self._lct_handler.get_super_clause_texts(),
                                DEFAULT_TEXT_SD,
                                list(self._conf["colors"]["alone"].values()),
                                raw_labels,
                                self._lct_handler.get_clause_tags()
                            )
                            self._actionSD.setChecked(True)
                            self._not_saved = False
                        elif len(raw_labels) == 2 and raw_labels[1] in DEFAULT_TEXT_SG:
                            self._current_file = file

                            self._classifierView.set_text_analyzed(
                                self._lct_handler.get_clause_texts(),
                                self._lct_handler.get_super_clause_texts(),
                                DEFAULT_TEXT_SD_SG,
                                list(self._conf["colors"]["together"].values()),
                                raw_labels,
                                self._lct_handler.get_clause_tags()
                            )
                            self._actionSD_SG.setChecked(True)
                            self._not_saved = False
                        else:
                            QMessageBox.critical(
                                self,
                                "File Error",
                                "The selected file has not valid content",
                                QMessageBox.Ok
                            )
                            self._lct_handler.unmount()
                            self._open_file_dialog(True)
                    else:
                        QMessageBox.critical(
                            self,
                            "File Error",
                            "The selected file has not valid content",
                            QMessageBox.Ok
                        )
                        self._lct_handler.unmount()
                        self._open_file_dialog(True)

    def _save_file_dialog(self, s: bool) -> bool:
        """
        Triggered when the user wants to save an existing analysis into an existing .lct file. If the analysis is not
        completed, an error dialog will be shown pointing that. If the .lct file doesn't exist yet, opens a new dialog
        to find the desired location and name for the .lct file.
        :param s: Button state. Non-relevant.
        :return: True if the file has been saved, False otherwise.
        """
        if self._current_file == "":
            return self._save_as_file_dialog(s)
        else:
            if self._lct_handler.upload_from_data(self._classifierView.get_text_analyzed()):
                manage_file(self._current_file, "w", self._lct_handler.to_string())
                QMessageBox.information(
                    self, "File Saved", "File saved in \"" + self._current_file + "\"", QMessageBox.Ok
                )
                self._not_saved = False
                return True
            else:
                QMessageBox.critical(
                    self, "Error", "The analysis is not completed (All '~' must be replaced)", QMessageBox.Ok
                )
                return False

    def _save_as_file_dialog(self, s: bool) -> bool:
        """
        Triggered when the user wants to save an existing analysis into a new .lct file. Opens a new dialog to find the
        desired location and name for the .lct file. If the analysis is not completed, an error dialog will be shown
        pointing that.
        :param s: Button state. Non-relevant.
        :return: True if the file has been saved, False otherwise.
        """
        if self._lct_handler.upload_from_data(self._classifierView.get_text_analyzed()):
            file, file_type = QFileDialog().getSaveFileName(
                self,
                "Save file",
                self._root_directory + "/analysis",
                "LCT Files (*.lct)"
            )
            if file != "":
                self._current_file = file
                manage_file(file, "w", self._lct_handler.to_string())
                self._not_saved = False
                return True
        else:
            QMessageBox.critical(
                self, "Error", "The analysis is not completed (All '~' must be replaced)", QMessageBox.Ok
            )
        return False

    def _text_size_dialog(self, s: bool) -> None:
        """
        Triggered when the user wants to change the text size of the text in the classifier. Opens a new dialog to
        select the desired point size of the text.
        :param s: Button state. Non-relevant.
        """
        value, ok = QInputDialog().getInt(
            self,
            "Change text size",
            "Text size:",
            self._classifierView.get_text_size(),
            4,  # Min value
            30,  # Max value
            1  # Step
        )

        if ok:
            self._classifierView.set_text_size(value)
            self._conf["text_size"] = value
            self._conf_has_changed = True

    def _rects_colors_dialog(self, s: bool) -> None:
        """
        Triggered when the user wants to change the background color of the rects in the classifier. Opens a new
        ColorsDialog to allow the user, change the desired background colors.
        :param s: Button state. Non-relevant.
        """
        dlg = ColorsDialog(self._conf["colors"], self)
        dlg.exec()

        if dlg.has_changed:
            self._conf["colors"] = dlg.colors
            if self._classifierView.get_default_descriptor() == DEFAULT_TEXT_SD_SG:
                self._classifierView.set_colors(list(self._conf["colors"]["together"].values()))
            else:
                self._classifierView.set_colors(list(self._conf["colors"]["alone"].values()))
            self._conf_has_changed = True

    def _target_action(self, text: str) -> None:
        """
        Triggered when the user wants to change the target in the classifier. Can be, SD, SG or SD and SG.
        :param text: The desired target. Can be DEFAULT_TEXT_SD_SG, DEFAULT_TEXT_SD or DEFAULT_TEXT_SG.
        """
        if text != self._classifierView.get_default_descriptor():
            if text == DEFAULT_TEXT_SD_SG:
                self._lct_handler.set_labels([SD_VALUES, SG_VALUES])
                self._classifierView.set_default_descriptor(text, list(self._conf["colors"]["together"].values()))
            elif text == DEFAULT_TEXT_SD:
                self._lct_handler.set_labels([SD_VALUES])
                self._classifierView.set_default_descriptor(text, list(self._conf["colors"]["alone"].values()))
            elif text == DEFAULT_TEXT_SG:
                self._lct_handler.set_labels([SG_VALUES])
                self._classifierView.set_default_descriptor(text, list(self._conf["colors"]["alone"].values()))

    def _split_in_sentences_action(self, s: bool) -> None:
        """
        Triggered when the user wants to split the text in the classifier in sentences. This functionality removes all
        the previous classifications.
        :param s: Button state. Non-relevant.
        """
        text = self._classifierView.get_text()
        split_text = SentenceSplitter().split_text(text)

        if self._actionSD.isChecked():
            self._classifierView.set_text_analyzed(
                split_text,
                [text],
                DEFAULT_TEXT_SD,
                list(self._conf["colors"]["alone"].values()),
                ["SD"],
                [[DEFAULT_DESCRIPTOR_VALUE] for _ in range(len(split_text))]
            )
        elif self._actionSG.isChecked():
            self._classifierView.set_text_analyzed(
                split_text,
                [text],
                DEFAULT_TEXT_SG,
                list(self._conf["colors"]["alone"].values()),
                ["SG"],
                [[DEFAULT_DESCRIPTOR_VALUE] for _ in range(len(split_text))]
            )
        elif self._actionSD_SG.isChecked():
            self._classifierView.set_text_analyzed(
                split_text,
                [text],
                DEFAULT_TEXT_SD_SG,
                list(self._conf["colors"]["together"].values()),
                ["SD", "SG"],
                [[DEFAULT_DESCRIPTOR_VALUE, DEFAULT_DESCRIPTOR_VALUE] for _ in range(len(split_text))]
            )

    def _run_graph_window(self, s: bool) -> None:
        """
        Triggered when the user wants to open the graph window to plot the analysis results. If the analysis is not
        completed, an error dialog will be shown pointing that.
        :param s: Button state. Non-relevant.
        """
        if self._lct_handler.upload_from_data(self._classifierView.get_text_analyzed()):
            self._graph_window.update_graphs(self._lct_handler)
            self._graph_window.show()
        else:
            QMessageBox.critical(
                self, "Error", "The analysis is not completed (All '~' must be replaced)", QMessageBox.Ok
            )

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        """
        This function handles the close event. If there are unsaved changes in the analysis, a dialog will be shown
        asking the user to save it. Also, if the user has changed the default configuration of the project (the text
        size and/or the background color of the RoundedRect) a dialog will be shown asking the user to save it.
        :param a0: The close event to handle.
        """
        close = False
        if self._not_saved:
            button = QMessageBox.question(
                self,
                "Save file",
                "Save changes in the file?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            if button == QMessageBox.Save:
                save = True
                while save and not self._save_file_dialog(True):
                    button = QMessageBox.question(
                        self,
                        "Save file",
                        "Save changes in the file?",
                        QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
                    )
                    if button == QMessageBox.Save:
                        save = True
                    else:
                        save = False
                close = True
            elif button == QMessageBox.Discard:
                close = True
            elif button == QMessageBox.Cancel:
                a0.ignore()
                return
        if self._conf_has_changed:
            button = QMessageBox.question(
                self,
                "Save settings",
                "Save current settings as default?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            if button == QMessageBox.Save:
                self.conf_data = json.dumps(self._conf)
                close = True
            elif button == QMessageBox.Discard:
                close = True
            elif button == QMessageBox.Cancel:
                a0.ignore()
                return

        if close or not (self._conf_has_changed and self._not_saved):
            super().closeEvent(a0)
            self._graph_window.close()

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
    def __init__(self, root_directory: str = "./", conf_file: str = None, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(':/icon/logo'))

        self.root_directory = root_directory

        self.current_file = ""

        self.lct_handler = LCTHandler("Semantics", [SD_VALUES, SG_VALUES])

        self.graph_window = GraphWindow(root_directory + "/graph/")
        if conf_file is not None:
            try:
                self.conf = json.loads(conf_file)
            except:
                file = QFile(":/conf/defconf")
                file.open(QFile.ReadOnly)
                self.conf = json.loads(QTextStream(file.readAll()).readAll())
        else:
            file = QFile(":/conf/defconf")
            file.open(QFile.ReadOnly)
            self.conf = json.loads(QTextStream(file.readAll()).readAll())

        self.conf_has_changed = False
        self.not_saved = False

        self.classifierView.setup(
            10,
            10,
            500,
            500,
            "This is an example text. If you want to start editing a file select \"File\"->\"Open...\" and browse to "
            "desired file.\nTo set a division in the text, right-click and select \"Split\". To undo a division in the "
            "text, right-click and select \"Join\" near the splitter.",
            self.conf["text_size"],
            DEFAULT_TEXT_SD_SG,
            DEFAULT_DESCRIPTOR_VALUE,
            ALLOWED_DESCRIPTOR_VALUES,
            list(self.conf["colors"]["together"].values())
        )
        self.classifierView.classifier.emitter.classifier_has_changed.connect(self.classifier_has_changed)

        self.actionNew.triggered.connect(self.new_file_dialog)
        self.actionOpen.triggered.connect(self.open_file_dialog)
        self.actionSave.triggered.connect(self.save_file_dialog)
        self.actionSave_as.triggered.connect(self.save_as_file_dialog)
        self.actionText_size.triggered.connect(self.text_size_dialog)
        self.actionRects_colors.triggered.connect(self.rects_colors_dialog)
        self.actionSD.triggered.connect(lambda checked: self.target_action(DEFAULT_TEXT_SD))
        self.actionSG.triggered.connect(lambda checked: self.target_action(DEFAULT_TEXT_SG))
        self.actionSD_SG.triggered.connect(lambda checked: self.target_action(DEFAULT_TEXT_SD_SG))
        self.actiongroupTarget.setExclusive(True)
        self.actionRun_Plotter.triggered.connect(self.run_graph_window)
        self.actionSplit_in_sentences.triggered.connect(self.split_in_sentences_action)

        self.conf_data = None

    def classifier_has_changed(self):
        self.not_saved = True

    def new_file_dialog(self, s: bool) -> None:
        file, file_type = QFileDialog().getOpenFileName(
            self,
            "Create new file from text file to analyze",
            self.root_directory,
            "Text files (*.txt)"
        )
        if file != "":
            text = manage_file(file, "r")
            if text is None or text == "":
                QMessageBox.critical(self, "File Error", "The selected file has not valid content", QMessageBox.Ok)
                self.new_file_dialog(True)
            else:
                self.current_file = ""
                self.classifierView.set_text(text)

    def open_file_dialog(self, s: bool) -> None:
        file, file_type = QFileDialog().getOpenFileName(
            self,
            "Open file to analyze",
            self.root_directory + "/analysis",
            "LCT Files (*.lct)"
        )
        if file != "":
            text = manage_file(file, "r")
            if text is None or text == "":
                QMessageBox.critical(self, "File Error", "The selected file has not valid content", QMessageBox.Ok)
                self.open_file_dialog(True)
            else:
                if not self.lct_handler.upload_from_xml_string(text, True):
                    QMessageBox.critical(self, "File Error", "The selected file has not valid content", QMessageBox.Ok)
                    self.open_file_dialog(True)
                else:

                    raw_labels = self.lct_handler.get_raw_labels()
                    if raw_labels[0] in DEFAULT_TEXT_SG:
                        self.current_file = file

                        self.classifierView.set_text_analyzed(
                            self.lct_handler.get_clause_texts(),
                            self.lct_handler.get_super_clause_texts(),
                            DEFAULT_TEXT_SG,
                            list(self.conf["colors"]["alone"].values()),
                            raw_labels,
                            self.lct_handler.get_clause_tags()
                        )
                        self.actionSG.setChecked(True)
                        self.not_saved = False
                    elif raw_labels[0] in DEFAULT_TEXT_SD:
                        if len(raw_labels) == 1:
                            self.current_file = file

                            self.classifierView.set_text_analyzed(
                                self.lct_handler.get_clause_texts(),
                                self.lct_handler.get_super_clause_texts(),
                                DEFAULT_TEXT_SD,
                                list(self.conf["colors"]["alone"].values()),
                                raw_labels,
                                self.lct_handler.get_clause_tags()
                            )
                            self.actionSD.setChecked(True)
                            self.not_saved = False
                        elif len(raw_labels) == 2 and raw_labels[1] in DEFAULT_TEXT_SG:
                            self.current_file = file

                            self.classifierView.set_text_analyzed(
                                self.lct_handler.get_clause_texts(),
                                self.lct_handler.get_super_clause_texts(),
                                DEFAULT_TEXT_SD_SG,
                                list(self.conf["colors"]["together"].values()),
                                raw_labels,
                                self.lct_handler.get_clause_tags()
                            )
                            self.actionSD_SG.setChecked(True)
                            self.not_saved = False
                        else:
                            QMessageBox.critical(
                                self,
                                "File Error",
                                "The selected file has not valid content",
                                QMessageBox.Ok
                            )
                            self.lct_handler.unmount()
                            self.open_file_dialog(True)
                    else:
                        QMessageBox.critical(
                            self,
                            "File Error",
                            "The selected file has not valid content",
                            QMessageBox.Ok
                        )
                        self.lct_handler.unmount()
                        self.open_file_dialog(True)

    def save_file_dialog(self, s: bool) -> bool:
        if self.current_file == "":
            return self.save_as_file_dialog(s)
        else:
            if self.lct_handler.upload_from_data(self.classifierView.get_text_analyzed()):
                manage_file(self.current_file, "w", self.lct_handler.to_string())
                QMessageBox.information(
                    self, "File Saved", "File saved in \"" + self.current_file + "\"", QMessageBox.Ok
                )
                self.not_saved = False
                return True
            else:
                QMessageBox.critical(
                    self, "Error", "The analysis is not completed (All '~' must be replaced)", QMessageBox.Ok
                )
                return False

    def save_as_file_dialog(self, s: bool) -> bool:
        if self.lct_handler.upload_from_data(self.classifierView.get_text_analyzed()):
            file, file_type = QFileDialog().getSaveFileName(
                self,
                "Save file",
                self.root_directory + "/analysis",
                "LCT Files (*.lct)"
            )
            if file != "":
                self.current_file = file
                manage_file(file, "w", self.lct_handler.to_string())
                self.not_saved = False
                return True
        else:
            QMessageBox.critical(
                self, "Error", "The analysis is not completed (All '~' must be replaced)", QMessageBox.Ok
            )
        return False

    def text_size_dialog(self, s: bool) -> None:
        value, ok = QInputDialog().getInt(
            self,
            "Change text size",
            "Text size:",
            self.classifierView.get_text_size(),
            4,  # Min value
            30,  # Max value
            1  # Step
        )

        if ok:
            self.classifierView.set_text_size(value)
            self.conf["text_size"] = value
            self.conf_has_changed = True

    def rects_colors_dialog(self, s: bool) -> None:
        dlg = ColorsDialog(self.conf["colors"], self)
        dlg.exec()

        if dlg.has_changed:
            self.conf["colors"] = dlg.colors
            if self.classifierView.get_default_descriptor() == DEFAULT_TEXT_SD_SG:
                self.classifierView.set_colors(list(self.conf["colors"]["together"].values()))
            else:
                self.classifierView.set_colors(list(self.conf["colors"]["alone"].values()))
            self.conf_has_changed = True

    def target_action(self, text: str) -> None:
        if text != self.classifierView.get_default_descriptor():
            if text == DEFAULT_TEXT_SD_SG:
                self.lct_handler.set_labels([SD_VALUES, SG_VALUES])
                self.classifierView.set_default_descriptor(text, list(self.conf["colors"]["together"].values()))
            elif text == DEFAULT_TEXT_SD:
                self.lct_handler.set_labels([SD_VALUES])
                self.classifierView.set_default_descriptor(text, list(self.conf["colors"]["alone"].values()))
            elif text == DEFAULT_TEXT_SG:
                self.lct_handler.set_labels([SG_VALUES])
                self.classifierView.set_default_descriptor(text, list(self.conf["colors"]["alone"].values()))

    def split_in_sentences_action(self, s: bool):
        text = self.classifierView.get_text()
        split_text = SentenceSplitter().split_text(text)

        if self.actionSD.isChecked():
            self.classifierView.set_text_analyzed(
                split_text,
                [text],
                DEFAULT_TEXT_SD,
                list(self.conf["colors"]["alone"].values()),
                ["SD"],
                [[DEFAULT_DESCRIPTOR_VALUE] for _ in range(len(split_text))]
            )
        elif self.actionSG.isChecked():
            self.classifierView.set_text_analyzed(
                split_text,
                [text],
                DEFAULT_TEXT_SG,
                list(self.conf["colors"]["alone"].values()),
                ["SG"],
                [[DEFAULT_DESCRIPTOR_VALUE] for _ in range(len(split_text))]
            )
        elif self.actionSD_SG.isChecked():
            self.classifierView.set_text_analyzed(
                split_text,
                [text],
                DEFAULT_TEXT_SD_SG,
                list(self.conf["colors"]["together"].values()),
                ["SD", "SG"],
                [[DEFAULT_DESCRIPTOR_VALUE, DEFAULT_DESCRIPTOR_VALUE] for _ in range(len(split_text))]
            )

    def run_graph_window(self, s: bool) -> None:
        if self.lct_handler.upload_from_data(self.classifierView.get_text_analyzed()):
            self.graph_window.update_graphs(self.lct_handler)
            self.graph_window.show()
        else:
            QMessageBox.critical(
                self, "Error", "The analysis is not completed (All '~' must be replaced)", QMessageBox.Ok
            )

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        close = False
        if self.not_saved:
            button = QMessageBox.question(
                self,
                "Save file",
                "Save changes in the file?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            if button == QMessageBox.Save:
                save = True
                while save and not self.save_file_dialog(True):
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
        if self.conf_has_changed:
            button = QMessageBox.question(
                self,
                "Save settings",
                "Save current settings as default?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            if button == QMessageBox.Save:
                self.conf_data = json.dumps(self.conf)
                close = True
            elif button == QMessageBox.Discard:
                close = True
            elif button == QMessageBox.Cancel:
                a0.ignore()
                return

        if close or not (self.conf_has_changed and self.not_saved):
            super().closeEvent(a0)
            self.graph_window.close()

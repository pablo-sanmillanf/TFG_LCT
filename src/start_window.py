import os
import sys
import traceback

from PyQt5 import QtGui
from PyQt5.QtCore import QStandardPaths, QDir, QSettings, QFile, QTextStream
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox

from app.main_window import MainWindow, manage_file
from startWindowQtCreator import Ui_StartWindow

from app.main_resources import main_resources


try:
    from ctypes import windll  # Only exists on Windows.
    myappid = 'mycompany.myproduct.subproduct.version'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass


class StartWindow(QMainWindow, Ui_StartWindow):
    def __init__(self, *args, **kwargs):
        super(StartWindow, self).__init__(*args, **kwargs)
        self._conf_file_path = None
        self._app_window = None
        self.setupUi(self)
        self.set_styles()

        self.setWindowIcon(QtGui.QIcon(':/icon/logo'))

        self.settings = QSettings("LCT", "Semantics Analyzer")

        self.default_location = self.settings.value(
            "workspace/root_dir",
            QStandardPaths.standardLocations(QStandardPaths.DocumentsLocation)[0]
        )

        self.pathText.setText(self.default_location)

        self.searchButton.clicked.connect(self.select_directory_dialog)
        self.buttonBox.accepted.connect(self.accept_slot)
        self.buttonBox.rejected.connect(self.reject_slot)

    def set_styles(self):
        self.pathText.setStyleSheet(
            "QLineEdit {"
            "    font-size: 13px;"
            "    border: 2px solid gray;"
            "    border-radius: 10px;"
            "    padding: 0 8px;"
            "    background: yellow;"
            "    selection-background-color: darkgray;"
            "}"
        )
        self.label.setStyleSheet(
            "QLabel, QToolTip {"
            "    font-size: 13px;"
            "    font-weight: bold;"
            "    padding: 2px;"
            "}"
        )
        self.title.setStyleSheet(
            "QLabel, QToolTip {"
            "    font-size: 15px;"
            "    font-weight: bold;"
            "    padding: 2px;"
            "}"
        )

    def select_directory_dialog(self, s: bool) -> None:
        if not QDir(self.pathText.text()).exists():
            location = self.default_location
        else:
            location = self.pathText.text()
        directory = QFileDialog().getExistingDirectory(
            self,
            "Open file to analyze",
            location,
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        if directory != "":
            self.pathText.setText(directory)

    def accept_slot(self) -> None:
        root_dir = self.pathText.text()
        if root_dir == "" or not QDir(root_dir).exists():
            QMessageBox.critical(self, "Directory Error", "This directory doesn't exists", QMessageBox.Ok)
            self.pathText.setText(self.default_location)
        else:
            self.settings.setValue("workspace/root_dir", root_dir)
            self.close()

            conf_file = None

            QDir().mkdir(os.path.join(root_dir, 'conf'))  # If dir already exists, do nothing

            self._conf_file_path = os.path.join(root_dir, 'conf/conf.conf')
            if not QFile.exists(self._conf_file_path):
                file = QFile(":/conf/defconf")
                file.open(QFile.ReadOnly)
                manage_file(self._conf_file_path, "w", QTextStream(file.readAll()).readAll())
            else:
                conf_file = manage_file(self._conf_file_path, "r")

            QDir().mkdir(os.path.join(root_dir, 'graph'))  # If dir already exists, do nothing

            QDir().mkdir(os.path.join(root_dir, 'analysis'))  # If dir already exists, do nothing

            self._app_window = MainWindow(self.pathText.text(), conf_file)
            self._app_window.show()

    def reject_slot(self) -> None:
        self.close()

    def save_conf(self):
        if self._app_window is not None and self._app_window.conf_data is not None:
            manage_file(self._conf_file_path, "w", self._app_window.conf_data)


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)

        sw = StartWindow()
        sw.show()

        app.exec()

        sw.save_conf()
    except Exception:
        open("./error.txt", "w", encoding="utf8").write(traceback.format_exc())
        print(traceback.format_exc())

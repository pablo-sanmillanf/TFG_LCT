import os
import sys
import traceback

from PyQt5 import QtGui
from PyQt5.QtCore import QStandardPaths, QDir, QSettings, QFile, QTextStream
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox

from main.main_window import MainWindow, manage_file
from startWindowQtCreator import Ui_StartWindow

from main.main_resources import main_resources


try:
    from ctypes import windll  # Only exists on Windows.
    myappid = 'mycompany.myproduct.subproduct.version'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass


class StartWindow(QMainWindow, Ui_StartWindow):
    """
    This class is used to select the default directory for the project. If the directory has not been used previously,
    this class will prepare it to be used by the MainWindow class.
    """
    def __init__(self) -> None:
        """
        Class constructor.
        """
        super(StartWindow, self).__init__()
        self._conf_file_path = None
        self._app_window = None
        self.setupUi(self)
        self._set_styles()

        self.setWindowIcon(QtGui.QIcon(':/icon/logo'))

        self._settings = QSettings("LCT", "Semantics Analyzer")

        self._default_location = self._settings.value(
            "workspace/root_dir",
            QStandardPaths.standardLocations(QStandardPaths.DocumentsLocation)[0]
        )

        self._pathText.setText(self._default_location)

        self._searchButton.clicked.connect(self._select_directory_dialog)
        self._buttonBox.accepted.connect(self._accept_slot)
        self._buttonBox.rejected.connect(self._reject_slot)

    def _set_styles(self) -> None:
        """
        Apply custom styles to the widgets in the window.
        """
        self._pathText.setStyleSheet(
            "QLineEdit {"
            "    font-size: 13px;"
            "    border: 2px solid gray;"
            "    border-radius: 10px;"
            "    padding: 0 8px;"
            # "    background: yellow;"
            "    selection-background-color: darkgray;"
            "}"
        )
        self._label.setStyleSheet(
            "QLabel, QToolTip {"
            "    font-size: 13px;"
            "    font-weight: bold;"
            "    padding: 2px;"
            "}"
        )
        self._title.setStyleSheet(
            "QLabel, QToolTip {"
            "    font-size: 15px;"
            "    font-weight: bold;"
            "    padding: 2px;"
            "}"
        )

    def _select_directory_dialog(self, s: bool) -> None:
        """
        Triggered when the user wants to select a directory to the project. Opens a new dialog to find the desired
        location for the project.
        :param s: Button state. Non-relevant.
        """
        if not QDir(self._pathText.text()).exists():
            location = self._default_location
        else:
            location = self._pathText.text()
        directory = QFileDialog().getExistingDirectory(
            self,
            "Open file to analyze",
            location,
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        if directory != "":
            self._pathText.setText(directory)

    def _accept_slot(self) -> None:
        """
        Triggered when the user has selected a valid directory to the project and wants to start the analysis. If the
        directory is a valid one, closes the StartWindow and opens the MainWindow to start the analysis. If the
        directory is not valid, an error dialog will be shown pointing that.
        """
        root_dir = self._pathText.text()
        if root_dir == "" or not QDir(root_dir).exists():
            QMessageBox.critical(self, "Directory Error", "This directory doesn't exists", QMessageBox.Ok)
            self._pathText.setText(self._default_location)
        else:
            self._settings.setValue("workspace/root_dir", root_dir)
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

            self._app_window = MainWindow(self._pathText.text(), conf_file)
            self._app_window.show()

    def _reject_slot(self) -> None:
        """
        Triggered when the user wants to close the application.
        """
        self.close()

    def save_conf(self) -> None:
        """
        If the configuration has been changed, saves it to replace the previous one.
        """
        if self._app_window is not None and self._app_window.conf_data is not None:
            manage_file(self._conf_file_path, "w", self._app_window.conf_data)


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)

        sw = StartWindow()
        sw.show()

        app.exec()

        sw.save_conf()
    except:
        open("./error.txt", "w", encoding="utf8").write(traceback.format_exc())
        print(traceback.format_exc())

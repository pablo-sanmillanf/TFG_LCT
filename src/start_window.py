import sys
import traceback

from PyQt5.QtCore import QStandardPaths, QDir
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox

from app.main_window import MainWindow
from startWindowQtCreator import Ui_StartWindow


try:
    from ctypes import windll  # Only exists on Windows.
    myappid = 'mycompany.myproduct.subproduct.version'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass


class StartWindow(QMainWindow, Ui_StartWindow):
    def __init__(self, *args, **kwargs):
        super(StartWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.set_styles()

        self.default_location = QStandardPaths.standardLocations(QStandardPaths.DocumentsLocation)[0]

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
        if not QDir(self.pathText.text()).exists():
            QMessageBox.critical(self, "Directory Error", "This directory doesn't exists", QMessageBox.Ok)
            self.pathText.setText(self.default_location)

    def reject_slot(self) -> None:
        self.close()


"""if __name__ == "__main__":
    app = QApplication(sys.argv)

    w = StartWindow()
    w.show()

    app.exec()"""


if __name__ == "__main__":
    app = QApplication(sys.argv)
    DEBUG = None

    if DEBUG is not None:

        try:
            w = MainWindow()
            w.show()

            app.exec()
        except Exception:
            open("./error.txt", "w", encoding="utf8").write(traceback.format_exc())
            print(traceback.format_exc())
    else:
        w = MainWindow()
        w.show()

        app.exec()

        if w.conf_data is not None:
            open("defaultconf.json", "w", encoding="utf8").write(w.conf_data)


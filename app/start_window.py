import sys

from PyQt5.QtCore import QStandardPaths, QDir
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox

from startWindowQtCreator import Ui_StartWindow

print("\n\n\n", )


class StartWindow(QMainWindow, Ui_StartWindow):
    def __init__(self, *args, **kwargs):
        super(StartWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.default_location = QStandardPaths.standardLocations(QStandardPaths.DocumentsLocation)[0]

        self.pathText.setText(self.default_location)

        self.searchButton.clicked.connect(self.select_directory_dialog)
        self.buttonBox.accepted.connect(self.accept_slot)
        self.buttonBox.rejected.connect(self.reject_slot)

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


if __name__ == "__main__":
    app = QApplication(sys.argv)

    w = StartWindow()
    w.show()

    app.exec()


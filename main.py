import sys


# QT importing
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from PyQt5.QtWidgets import QSizePolicy, QFileDialog
from PyQt5.QtGui import QPixmap, QImage


MAIN_UI_FILE = r"UI\main_ui.ui"


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(MAIN_UI_FILE, self)
        self.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

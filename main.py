import sys


# QT importing
from PyQt5 import QtWidgets, uic


# our libs importing
from api import api


MAIN_UI_FILE = "UI/main_ui.ui"


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(MAIN_UI_FILE, self)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    API = api(ui_obj=window)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

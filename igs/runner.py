import sys

from PyQt5 import QtWidgets

from igs.ui.main_window import MainWindow


def main():
    app = QtWidgets.QApplication(sys.argv)

    ui = MainWindow()
    ui.show()

    app.exec()


if __name__ == "__main__":
    main()

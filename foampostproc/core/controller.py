import sys
import random
from typing import List, Callable

from PySide6 import QtWidgets as QtW, QtCore as QtC
from PySide6.QtWidgets import QAbstractItemView

from foampostproc.core.model import Point
from foampostproc.core.view import MainWidget

WINDOW_X, WINDOW_Y, WINDOW_W, WINDOW_H = 10, 10, 1000, 800
WINDOW_TITLE = "App"

class Controller(object):
    pass


if __name__ == "__main__":
    app = QtW.QApplication(sys.argv)
    window = QtW.QMainWindow()

    layout = QtW.QGridLayout()
    central_widget = QtW.QWidget()
    central_widget.setLayout(layout)
    layout.addWidget(MainWidget(["case1", "case2", "case3"], None, None, None, None, None, None, None, None, None,
                                None, None, None, None))
    window.setCentralWidget(central_widget)

    window.setWindowTitle(WINDOW_TITLE)
    window.setGeometry(WINDOW_X, WINDOW_Y, WINDOW_W, WINDOW_H)
    window.show()
    sys.exit(app.exec_())

import sys
import random
from typing import List

from PySide6 import QtWidgets as QtW, QtCore as QtC, QtGui as QtG
from PySide6.QtWidgets import QAbstractItemView

WINDOW_X, WINDOW_Y, WINDOW_W, WINDOW_H = 10, 10, 1000, 800
WINDOW_TITLE = "App"


class ControlList(QtW.QWidget):
    def __init__(self, name: str, list_items: List[str]):
        super().__init__()

        self.header = self._create_header(name)
        self.list_ = self._create_list(list_items)

        self.setLayout(QtW.QVBoxLayout())
        self.layout().addWidget(self.header)
        self.layout().addSpacing(4)
        self.layout().addWidget(self.list_)

    def _create_header(self, name: str) -> QtW.QWidget:
        header_widget = QtW.QWidget()
        header_layout = QtW.QHBoxLayout()
        header_widget.setLayout(header_layout)

        header_widget.label = QtW.QLabel(name)

        header_widget.add_button = QtW.QPushButton("Добавить")
        header_widget.add_button.clicked.connect(self.handle_header_add_button)


        header_widget.remove_button = QtW.QPushButton("Удалить")
        header_widget.add_button.clicked.connect(self.handle_header_remove_button)
        header_layout.addWidget(header_widget.label)
        header_layout.addSpacing(4)
        header_layout.addWidget(header_widget.add_button)
        header_layout.addWidget(header_widget.remove_button)

        return header_widget

    def _create_list(self, list_items: List[str]) -> QtW.QListWidget:
        list_ = QtW.QListWidget()
        list_.setAlternatingRowColors(True)
        list_.setSelectionMode(QAbstractItemView.SingleSelection)
        list_.addItems(list_items)
        list_.itemSelectionChanged.connect(self.handle_item_selection_changed)
        return list_

    @QtC.Slot()
    def handle_header_add_button(self):
        print("header_add_button")

    @QtC.Slot()
    def handle_header_remove_button(self):
        print("header_remove_button")

    @QtC.Slot()
    def handle_item_selection_changed(self):
        print("handle_item_selection_changed")


def run_ui():
    app = QtW.QApplication(sys.argv)
    window = QtW.QMainWindow()

    layout = QtW.QGridLayout()
    central_widget = QtW.QWidget()
    central_widget.setLayout(layout)
    layout.addWidget(ControlList("Cases", ["case1", "case2", "case3"]))
    window.setCentralWidget(central_widget)

    window.setWindowTitle(WINDOW_TITLE)
    window.setGeometry(WINDOW_X, WINDOW_Y, WINDOW_W, WINDOW_H)
    window.show()
    sys.exit(app.exec_())


class MyWidget(QtW.QWidget):
    def __init__(self):
        super().__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.button = QtW.QPushButton("Click me!")
        self.text = QtW.QLabel("Hello World",
                                     alignment=QtC.Qt.AlignCenter)

        self.layout = QtW.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)

    @QtC.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))


if __name__ == "__main__":
    run_ui()
    # app = QtW.QApplication([])
    #
    # widget = MyWidget()
    # widget.resize(800, 600)
    # widget.show()
    #
    # sys.exit(app.exec_())

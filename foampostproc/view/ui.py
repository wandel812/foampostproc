import sys
import random
from typing import List, Callable

from PySide6 import QtWidgets as QtW, QtCore as QtC, QtGui as QtG
from PySide6.QtWidgets import QAbstractItemView

WINDOW_X, WINDOW_Y, WINDOW_W, WINDOW_H = 10, 10, 1000, 800
WINDOW_TITLE = "App"


class ControlList(QtW.QWidget):
    LABEL_SPACING = 4

    def __init__(self, name: str, list_items: List[str]):
        super().__init__()

        self.header = self._create_header(name)
        self.list_ = self._create_list(list_items)

        self.setLayout(QtW.QVBoxLayout())
        self.layout().addWidget(self.header)
        self.layout().addSpacing(self.LABEL_SPACING)
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


class ParamsForm(QtW.QWidget):
    def __init__(self, list_items):
        super().__init__()
        self.list_ = QtW.QListWidget()
        self.list_.setAlternatingRowColors(True)
        self.list_.setSelectionMode(QAbstractItemView.SingleSelection)
        self.list_.addItems(list_items)
        self.list_.itemSelectionChanged.connect(self.handle_item_selection_changed)


class TextEdit(QtW.QWidget):
    LABEL_SPACING = 4

    def __init__(self, label_text: str, handleOnTextChanged: Callable, edit_text: str = ""):
        super().__init__()
        self.handleOnTextChanged = handleOnTextChanged

        self.label = QtW.QLabel(label_text)
        self.text_edit = QtW.QLineEdit(edit_text)
        self.text_edit.textChanged[str].connect(self._handleOnTextChanged)

        self.setLayout(QtW.QHBoxLayout())
        self.layout().addWidget(self.label)
        self.layout().addSpacing(self.LABEL_SPACING)
        self.layout().addWidget(self.text_edit)

    @QtC.Slot(str)
    def _handleOnTextChanged(self, text):
        self.handleOnTextChanged(text)


class PointTextEdit(QtW.QWidget):
    def __init__(self, label_text: str,
                 handle_on_text_changed1: Callable,
                 handle_on_text_changed2: Callable,
                 handle_on_text_changed3: Callable,
                 text1: str = "",
                 text2: str = "",
                 text3: str = ""
                 ):
        super().__init__()
        self._handle_on_text_changed1 = handle_on_text_changed1
        self._handle_on_text_changed2 = handle_on_text_changed2
        self._handle_on_text_changed3 = handle_on_text_changed3

        self.label = QtW.QLabel(label_text)
        self.text_edit1 = QtW.QLineEdit(text1)
        self.text_edit1.textChanged[str].connect(self._handle_on_text_changed1)
        self.text_edit2 = QtW.QLineEdit(text2)
        self.text_edit2.textChanged[str].connect(self._handle_on_text_changed2)
        self.text_edit3 = QtW.QLineEdit(text3)
        self.text_edit3.textChanged[str].connect(self._handle_on_text_changed3)

        self.setLayout(QtW.QHBoxLayout())
        self.layout().addWidget(self.label)
        self.layout().addSpacing(self.LABEL_SPACING)
        self.layout().addWidget(self.text_edit)

    @QtC.Slot(str)
    def _handleOnTextChanged1(self, text):
        self._handle_on_text_changed1(text)

    @QtC.Slot(str)
    def _handleOnTextChanged2(self, text):
        self._handle_on_text_changed2(text)

    @QtC.Slot(str)
    def _handleOnTextChanged3(self, text):
        self._handle_on_text_changed3(text)


def run_ui():
    app = QtW.QApplication(sys.argv)
    window = QtW.QMainWindow()

    layout = QtW.QGridLayout()
    central_widget = QtW.QWidget()
    central_widget.setLayout(layout)
    layout.addWidget(TextEdit("case_path", lambda text: print(f"text_edit: {text}")))
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

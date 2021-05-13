import sys
import random
from typing import List, Callable

from PySide6 import QtWidgets as QtW, QtCore as QtC
from PySide6.QtWidgets import QAbstractItemView

from foampostproc.core.model import Point

WINDOW_X, WINDOW_Y, WINDOW_W, WINDOW_H = 10, 10, 1000, 800
WINDOW_TITLE = "App"


class ControlList(QtW.QWidget):
    ADD_BUTTON_TEXT = "Добавить"
    RM_BUTTON_TEXT = "Удалить"
    LABEL_SPACING = 4
    ALTERNATING_ROW_COLORS = True

    def __init__(self, label_text: str, list_items: List[str],
                 on_add_button_clicked: Callable,
                 on_rm_button_clicked: Callable,
                 on_item_selection: Callable):
        super().__init__()
        self.on_add_button_clicked = on_add_button_clicked
        self.on_rm_button_clicked = on_rm_button_clicked
        self.on_item_selection = on_item_selection

        self.header = self._create_header(label_text)
        self.list_ = self._create_list(list_items)

        self.setLayout(QtW.QVBoxLayout())
        self.layout().addWidget(self.header)
        self.layout().addSpacing(self.LABEL_SPACING)
        self.layout().addWidget(self.list_)

    def _create_header(self, label_text: str) -> QtW.QWidget:
        header_widget = QtW.QWidget()
        header_layout = QtW.QHBoxLayout()
        header_widget.setLayout(header_layout)

        header_widget.label = QtW.QLabel(label_text)

        header_widget.add_button = Button(self.ADD_BUTTON_TEXT, self.handle_header_add_button)
        header_widget.remove_button = Button(self.RM_BUTTON_TEXT, self.handle_header_remove_button)

        header_layout.addWidget(header_widget.label)
        header_layout.addSpacing(4)
        header_layout.addWidget(header_widget.add_button)
        header_layout.addWidget(header_widget.remove_button)

        return header_widget

    def _create_list(self, list_items: List[str]) -> QtW.QListWidget:
        list_ = QtW.QListWidget()
        list_.setAlternatingRowColors(self.ALTERNATING_ROW_COLORS)
        list_.setSelectionMode(QAbstractItemView.SingleSelection)
        list_.addItems(list_items)
        list_.itemSelectionChanged.connect(self.handle_item_selection_changed)
        return list_

    @QtC.Slot()
    def handle_header_add_button(self):
        print()

    @QtC.Slot()
    def handle_header_remove_button(self):
        print("header_remove_button")

    @QtC.Slot()
    def handle_item_selection_changed(self):
        print("handle_item_selection_changed")


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
    SPACING = 4

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
        self.layout().addSpacing(self.SPACING)
        self.layout().addWidget(self.text_edit1)
        self.layout().addSpacing(self.SPACING)
        self.layout().addWidget(self.text_edit2)
        self.layout().addSpacing(self.SPACING)
        self.layout().addWidget(self.text_edit3)

    @QtC.Slot(str)
    def _handleOnTextChanged1(self, text):
        self._handle_on_text_changed1(text)

    @QtC.Slot(str)
    def _handleOnTextChanged2(self, text):
        self._handle_on_text_changed2(text)

    @QtC.Slot(str)
    def _handleOnTextChanged3(self, text):
        self._handle_on_text_changed3(text)


class CameraParamsForm(QtW.QWidget):
    POSITION_FIELD_TEXT = "         Позиция"
    FOCAL_POINT_FIELD_TEXT = "Точка фокуса"
    VIEW_ANGLE_FIELD_TEXT = "  Угол обзора"
    VIEW_UP_TEXT = "Наклон"

    SPACING = 4

    def __init__(self):
        super().__init__()
        self.setLayout(QtW.QVBoxLayout())

        self.position = Point(0, 0, 0)
        self._position_field = PointTextEdit(self.POSITION_FIELD_TEXT,
                                             lambda text: self.position.__setattr__("x", int(text)),
                                             lambda text: self.position.__setattr__("y", int(text)),
                                             lambda text: self.position.__setattr__("z", int(text)))

        self.focal_point = Point(0, 0, 0)
        self._focal_point_field = PointTextEdit(self.FOCAL_POINT_FIELD_TEXT,
                                                lambda text: self.focal_point.__setattr__("x", int(text)),
                                                lambda text: self.focal_point.__setattr__("y", int(text)),
                                                lambda text: self.focal_point.__setattr__("z", int(text)))

        self.view_angle = Point(0, 0, 0)
        self._view_angle_field = PointTextEdit(self.VIEW_ANGLE_FIELD_TEXT,
                                               lambda text: self.view_angle.__setattr__("x", int(text)),
                                               lambda text: self.view_angle.__setattr__("y", int(text)),
                                               lambda text: self.view_angle.__setattr__("z", int(text)))

        self._view_up = [0]
        self._view_up_field = TextEdit(self.VIEW_UP_TEXT, lambda text: self._view_up.__setitem__(0, int(text)))

        self.setLayout(QtW.QVBoxLayout())
        self.layout().addWidget(self._position_field)
        self.layout().addSpacing(self.SPACING)
        self.layout().addWidget(self._focal_point_field)
        self.layout().addSpacing(self.SPACING)
        self.layout().addWidget(self._view_angle_field)
        self.layout().addSpacing(self.SPACING)
        self.layout().addWidget(self._view_up_field)

    @property
    def view_up(self):
        return self._view_up[0]

    @view_up.setter
    def view_up(self, value):
        self._view_up[0] = value


class SliceParamsForm(QtW.QWidget):
    X_SLICE_LABEL_TEXT = "Срез X"
    Y_SLICE_LABEL_TEXT = "Срез Y"
    Z_SLICE_LABEL_TEXT = "Срез Z"
    X_LABEL_TEXT = "x"
    Y_LABEL_TEXT = "y"
    Z_LABEL_TEXT = "z"

    SPACING = 4

    def __init__(self):
        super().__init__()
        self.setLayout(QtW.QVBoxLayout())

        self.x_slice = Point(0, 0, 0)
        self._x_slice_field = PointTextEdit(self.X_SLICE_LABEL_TEXT,
                                            lambda text: self.x_slice.__setattr__(self.X_LABEL_TEXT, int(text)),
                                            lambda text: self.x_slice.__setattr__(self.Y_LABEL_TEXT, int(text)),
                                            lambda text: self.x_slice.__setattr__(self.Z_LABEL_TEXT, int(text)))

        self.y_slice = Point(0, 0, 0)
        self._y_slice_field = PointTextEdit(self.Y_SLICE_LABEL_TEXT,
                                            lambda text: self.y_slice.__setattr__(self.X_LABEL_TEXT, int(text)),
                                            lambda text: self.y_slice.__setattr__(self.Y_LABEL_TEXT, int(text)),
                                            lambda text: self.y_slice.__setattr__(self.Z_LABEL_TEXT, int(text)))

        self.z_slice = Point(0, 0, 0)
        self._z_slice_field = PointTextEdit(self.Z_SLICE_LABEL_TEXT,
                                            lambda text: self.z_slice.__setattr__(self.X_LABEL_TEXT, int(text)),
                                            lambda text: self.z_slice.__setattr__(self.Y_LABEL_TEXT, int(text)),
                                            lambda text: self.z_slice.__setattr__(self.Z_LABEL_TEXT, int(text)))

        self.setLayout(QtW.QVBoxLayout())
        self.layout().addWidget(self._x_slice_field)
        self.layout().addSpacing(self.SPACING)
        self.layout().addWidget(self._y_slice_field)
        self.layout().addSpacing(self.SPACING)
        self.layout().addWidget(self._z_slice_field)


class Button(QtW.QPushButton):
    def __init__(self, button_text: str, handle_on_click: Callable):
        super().__init__(button_text)
        self.handle_on_click = handle_on_click
        self.clicked.connect(self._handle_on_click)

    @QtC.Slot()
    def _handle_on_click(self):
        self.handle_on_click()


class SaveResetButtonGroup(QtW.QWidget):
    def __init__(self, save_btn_txt: str, handle_save: Callable, reset_btn_text: str, handle_reset: Callable):
        super().__init__()
        self.handle_save = handle_save
        self.handle_reset = handle_reset

        self.setLayout(QtW.QHBoxLayout())
        self.button_save = Button(save_btn_txt, self.handle_save)
        self.button_reset = Button(reset_btn_text, self.handle_reset)

        self.layout().addWidget(self.button_reset)
        self.layout().addSpacing(4)
        self.layout().addWidget(self.button_save)

    @QtC.Slot()
    def _handle_save(self):
        self.handle_save()

    @QtC.Slot()
    def _handle_reset(self):
        self.handle_reset()


class MainWidget(QtW.QWidget):
    SPACING = 4
    CASES_LABEL = "Примеры"
    GENERATE_BTN_TEXT = "Генерация"
    CAMERA_PROPS_LABEL = "Свойсва камеры"
    SLICE_PROPS_LABEL = "Срезы"
    CASE_PATH_FIELD_TEXT = "Путь"
    SAVE_BTN_TEXT = "Сохранить"
    RESET_BTN_TEXT = "Сбросить"

    def __init__(self, case_list: List[str],
                 handle_cases_add_button_clicked,
                 handle_cases_rm_button_clicked,
                 handle_cases_item_selection,
                 handle_generate_button_clicked,
                 handle_case_path_field_on_text_changed,
                 handle_camera_props_add_button_clicked,
                 handle_camera_props_rm_button_clicked,
                 handle_camera_props_item_selection,
                 handle_slice_props_add_button_clicked,
                 handle_slice_props_rm_button_clicked,
                 handle_slice_props_item_selection,
                 handle_save_btn,
                 handle_reset_btn,
                 ):
        super().__init__()

        # first col ----------------------------------------------
        self.handle_cases_add_button_clicked = handle_cases_add_button_clicked
        self.handle_cases_rm_button_clicked = handle_cases_rm_button_clicked
        self.handle_cases_item_selection = handle_cases_item_selection
        self.handle_generate_button_clicked = handle_generate_button_clicked

        first_col_widget = QtW.QWidget()
        first_col_widget.setLayout(QtW.QVBoxLayout())
        cases_control_list = ControlList(self.CASES_LABEL, case_list,
                                         self.handle_cases_add_button_clicked,
                                         self.handle_cases_rm_button_clicked,
                                         self.handle_cases_item_selection)
        generate_button = Button(self.GENERATE_BTN_TEXT, self.handle_generate_button_clicked)
        first_col_widget.layout().addWidget(cases_control_list)
        first_col_widget.layout().addWidget(generate_button)

        # second col ---------------------------------------------
        self.handle_case_path_field_on_text_changed = handle_case_path_field_on_text_changed
        self.case_path_field = TextEdit(self.CASE_PATH_FIELD_TEXT, self.handle_case_path_field_on_text_changed)

        self.handle_camera_props_add_button_clicked = handle_camera_props_add_button_clicked
        self.handle_camera_props_rm_button_clicked = handle_camera_props_rm_button_clicked
        self.handle_camera_props_item_selection = handle_camera_props_item_selection
        self.camera_props_control_list = ControlList(self.CAMERA_PROPS_LABEL, [],
                                                     self.handle_camera_props_add_button_clicked,
                                                     self.handle_camera_props_rm_button_clicked,
                                                     self.handle_camera_props_item_selection)
        self.camera_props_params_form = CameraParamsForm()

        self.handle_slice_props_add_button_clicked = handle_slice_props_add_button_clicked
        self.handle_slice_props_rm_button_clicked = handle_slice_props_rm_button_clicked
        self.handle_slice_props_item_selection = handle_slice_props_item_selection
        self.slice_props_control_list = ControlList(self.SLICE_PROPS_LABEL, [],
                                                    self.handle_slice_props_add_button_clicked,
                                                    self.handle_slice_props_rm_button_clicked,
                                                    self.handle_slice_props_item_selection)
        self.slice_params_form = SliceParamsForm()

        self.handle_save_btn = handle_save_btn
        self.handle_reset_btn = handle_reset_btn
        self.save_reset_btn_group = SaveResetButtonGroup(self.SAVE_BTN_TEXT, self.handle_save_btn, self.RESET_BTN_TEXT,
                                                         self.handle_reset_btn)

        second_col_widget = QtW.QWidget()
        second_col_widget.setLayout(QtW.QVBoxLayout())
        second_col_widget.layout().addWidget(self.case_path_field)
        second_col_widget.layout().addSpacing(self.SPACING)

        first_row_second_col_widget = QtW.QWidget()
        first_row_second_col_widget.setLayout(QtW.QHBoxLayout())
        first_row_second_col_widget.layout().addWidget(self.camera_props_control_list)
        first_row_second_col_widget.layout().addSpacing(self.SPACING)
        first_row_second_col_widget.layout().addWidget(self.camera_props_params_form)
        second_col_widget.layout().addWidget(first_row_second_col_widget)

        second_row_second_col_widget = QtW.QWidget()
        second_row_second_col_widget.setLayout(QtW.QVBoxLayout())
        second_row_second_col_widget.layout().addWidget(self.slice_props_control_list)
        second_row_second_col_widget.layout().addWidget(self.slice_params_form)
        second_col_widget.layout().addWidget(second_row_second_col_widget)

        second_col_widget.layout().addWidget(self.save_reset_btn_group)

        self.setLayout(QtW.QHBoxLayout())
        self.layout().addWidget(first_col_widget)
        self.layout().addWidget(second_col_widget)


# ---------------------------- control _____________________________________


def run_ui():
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

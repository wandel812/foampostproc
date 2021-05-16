from paraview.simple import *
from PySide6 import QtWidgets as QtW

import foampostproc.dto.dto as dto
from foampostproc.config import Config
from foampostproc.core.controller import handlers
from foampostproc.core.screenshot.taker import Screenshot
from foampostproc.core.view import MainWidget
from foampostproc.dao.dao import MongoFoamCaseDAO
from foampostproc.dao.daofactory import MongoDaoFactory
from foampostproc.utils import FileHandling, SharedState
from foampostproc.dto.modelmapper import Mapper

# https://docs.paraview.org/en/v5.8.1/UsersGuide/displayingData.html?highlight=slice#slice-view

WINDOW_X = Config.get_section("ViewProperties").get_int("window_x")
WINDOW_Y = Config.get_section("ViewProperties").get_int("window_y")
WINDOW_W = Config.get_section("ViewProperties").get_int("window_w")
WINDOW_H = Config.get_section("ViewProperties").get_int("window_h")
WINDOW_TITLE = Config.get_section("ViewProperties").get("window_title")
TEST_DATA_PATH = Config.get_section("Paths").get_path("test_data")


def __run0():
    case_dto = FileHandling.read_json(TEST_DATA_PATH, object_hook_=dto.parse_config_json_hook)


def __run1():
    case_dtos = MongoDaoFactory().get_dao(MongoFoamCaseDAO).get_all()
    cases = list(map(Mapper.map_foam_case_dto, case_dtos))
    Screenshot.take_screenshots(cases, Config.get_section("Paths").get_path("output"))


def run():
    case_dtos = MongoDaoFactory().get_dao(MongoFoamCaseDAO).get_all()
    cases = list(map(Mapper.map_foam_case_dto, case_dtos))

    app = QtW.QApplication(sys.argv)

    window = QtW.QMainWindow()
    m_widget = MainWidget([case.name for case in cases], **handlers)
    SharedState.m_widget = m_widget
    SharedState.case_list = cases

    layout = QtW.QGridLayout()
    central_widget = QtW.QWidget()
    central_widget.setLayout(layout)
    layout.addWidget(m_widget)
    window.setCentralWidget(central_widget)

    window.setWindowTitle(WINDOW_TITLE)
    window.setGeometry(WINDOW_X, WINDOW_Y, WINDOW_W, WINDOW_H)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()

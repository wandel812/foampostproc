from paraview.simple import *
from PySide6 import QtWidgets as QtW, QtCore as QtC

import foampostproc.dto.dto as dto
from foampostproc.core.controller import handlers
from foampostproc.core.screenshot.taker import Screenshot
from foampostproc.core.view import MainWidget
from foampostproc.dao.dao import MongoFoamCaseDAO
from foampostproc.dao.daofactory import MongoDaoFactory
from foampostproc.utils import FileHandling, PROJ_DIR, OTP_DIR, SharedState
from foampostproc.dto.modelmapper import Mapper

# https://docs.paraview.org/en/v5.8.1/UsersGuide/displayingData.html?highlight=slice#slice-view

WINDOW_X, WINDOW_Y, WINDOW_W, WINDOW_H = 10, 10, 1000, 800
WINDOW_TITLE = "App"


def run0():
    case_dto = FileHandling.read_json(PROJ_DIR / "config/conf.json",
                                      object_hook_=dto.parse_config_json_hook)


def run1():
    case_dtos = MongoDaoFactory().get_dao(MongoFoamCaseDAO).get_all()
    cases = list(map(Mapper.map_foam_case_dto, case_dtos))
    Screenshot.take_screenshots(cases, OTP_DIR)


def run2():
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
    run2()

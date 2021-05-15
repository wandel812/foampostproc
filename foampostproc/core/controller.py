from copy import deepcopy
from pathlib import Path

from PySide6 import QtWidgets as QtW, QtCore as QtC
from bson import ObjectId

from foampostproc.config import Config
from foampostproc.core.model import Point, FoamCase, CasesDir, CameraProps, CameraSlice
from foampostproc.core.screenshot.taker import Screenshot
from foampostproc.dao.dao import MongoFoamCaseDAO, MongoCameraPropsDAO, MongoCameraSliceDAO
from foampostproc.dao.daofactory import MongoDaoFactory
from foampostproc.dto.modelmapper import Mapper
from foampostproc.utils import SharedState


def handle_cases_add_button_clicked():
    case_dir = CasesDir(ObjectId(), "")
    foamcase = FoamCase(ObjectId(), f"case{len(SharedState.case_list) + 1}", case_dir, [], [])
    SharedState.case_list.append(foamcase)
    SharedState.m_widget.cases_control_list.list_.addItem(foamcase.name)
    if len(SharedState.case_list) - 1 > 0:
        SharedState.m_widget.cases_control_list.list_.setCurrentRow(len(SharedState.case_list) - 1)
    handle_camera_props_add_button_clicked()


def handle_cases_rm_button_clicked():
    list_ = SharedState.m_widget.cases_control_list.list_
    for item in list_.selectedItems():
        item_row = list_.row(item)
        SharedState.cases_for_del.append(SharedState.case_list[item_row])
        SharedState.case_list.pop(item_row)
        list_.takeItem(item_row)
    if len(SharedState.case_list) - 1 > 0:
        list_.setCurrentRow(len(SharedState.case_list) - 1)


def handle_cases_item_selection():
    case = _get_selected_case()
    list_ = SharedState.m_widget.camera_props_control_list.list_
    SharedState.m_widget.camera_props_params_form.clear()
    list_.clear()
    list_.addItems([prop.name for prop in case.cam_prop_list])
    list_.setCurrentRow(0)
    handle_camera_props_item_selection()

    #
    # list_ = SharedState.m_widget.slice_props_control_list.list_
    # SharedState.m_widget.slice_params_form.clear()
    # list_.clear()
    # list_.addItems([prop.name for prop in case.slice_list])
    # list_.setCurrentRow(0)

    SharedState.m_widget.case_path_field.clear()

    SharedState.m_widget.case_path_field.text_edit.setText(str(case.cases_dir.path))


def handle_generate_button_clicked():
    Screenshot.take_screenshots(SharedState.case_list, Config.get_section("Paths").get_path("output"))


def handle_case_path_field_on_text_changed():
    pass


def handle_camera_props_add_button_clicked():
    case = _get_selected_case()
    cam_prop = CameraProps(ObjectId(), f"camera{len(case.cam_prop_list) + 1}", Point(0, 0, 0),
                           Point(0, 0, 0), 0, Point(0, 0, 0))
    case.cam_prop_list.append(cam_prop)
    SharedState.m_widget.camera_props_control_list.list_.addItem(cam_prop.name)
    if len(case.cam_prop_list) - 1 > 0:
        SharedState.m_widget.camera_props_control_list.list_.setCurrentRow(len(case.cam_prop_list) - 1)


def handle_camera_props_rm_button_clicked():
    case = _get_selected_case()

    list_ = SharedState.m_widget.camera_props_control_list.list_
    for item in list_.selectedItems():
        item_row = list_.row(item)
        SharedState.cam_props_for_del.append(case.cam_prop_list[item_row])
        case.cam_prop_list.pop(item_row)
        list_.takeItem(item_row)
    if len(case.cam_prop_list) - 1 > 0:
        list_.setCurrentRow(len(case.cam_prop_list) - 1)


def handle_camera_props_item_selection():
    # if len(_get_selected_case().slice_list) == 0 or len(_get_selected_case().cam_prop_list) == 0:
    #     return

    cam_prop = _get_selected_cam_prop()
    if cam_prop is not None:
        form = SharedState.m_widget.camera_props_params_form
        form.position_field.text_edit1.setText(str(cam_prop.cam_position.x))
        form.position_field.text_edit2.setText(str(cam_prop.cam_position.y))
        form.position_field.text_edit3.setText(str(cam_prop.cam_position.z))

        form.focal_point_field.text_edit1.setText(str(cam_prop.focal_point.x))
        form.focal_point_field.text_edit2.setText(str(cam_prop.focal_point.y))
        form.focal_point_field.text_edit3.setText(str(cam_prop.focal_point.z))

        form.view_up_field.text_edit1.setText(str(cam_prop.viewup.x))
        form.view_up_field.text_edit2.setText(str(cam_prop.viewup.y))
        form.view_up_field.text_edit3.setText(str(cam_prop.viewup.z))

        form.view_angle_field.text_edit.setText(str(cam_prop.viewangle))


def handle_slice_props_add_button_clicked():
    case = _get_selected_case()
    cam_slice = CameraSlice(ObjectId(), f"slice{len(case.slice_list) + 1}", None, None, None)
    case.slice_list.append(cam_slice)
    SharedState.m_widget.slice_props_control_list.list_.addItem(cam_slice.name)
    if len(case.slice_list) - 1 > 0:
        SharedState.m_widget.slice_props_control_list.list_.setCurrentRow(len(case.slice_list) - 1)


def handle_slice_props_rm_button_clicked():
    case = _get_selected_case()

    list_ = SharedState.m_widget.slice_props_control_list.list_
    for item in list_.selectedItems():
        item_row = list_.row(item)
        SharedState.slices_for_del.append(case.slice_list[item_row])
        case.slice_list.pop(item_row)
        list_.takeItem(item_row)
    if len(case.slice_list) - 1 > 0:
        list_.setCurrentRow(len(case.slice_list) - 1)


def handle_slice_props_item_selection():
    slice_ = _get_selected_slice_prop()

    if slice_ is not None:
        form = SharedState.m_widget.slice_params_form

        x = "" if slice_.sl_x is None else str(slice_.sl_x.x)
        y = "" if slice_.sl_x is None else str(slice_.sl_x.y)
        z = "" if slice_.sl_x is None else str(slice_.sl_x.z)

        form.x_slice_field.text_edit1.setText(x)
        form.x_slice_field.text_edit2.setText(y)
        form.x_slice_field.text_edit3.setText(z)

        x = "" if slice_.sl_y is None else str(slice_.sl_y.x)
        y = "" if slice_.sl_y is None else str(slice_.sl_y.y)
        z = "" if slice_.sl_y is None else str(slice_.sl_y.z)

        form.y_slice_field.text_edit1.setText(x)
        form.y_slice_field.text_edit2.setText(y)
        form.y_slice_field.text_edit3.setText(z)

        x = "" if slice_.sl_z is None else str(slice_.sl_z.x)
        y = "" if slice_.sl_z is None else str(slice_.sl_z.y)
        z = "" if slice_.sl_z is None else str(slice_.sl_z.z)

        form.z_slice_field.text_edit1.setText(x)
        form.z_slice_field.text_edit2.setText(y)
        form.z_slice_field.text_edit3.setText(z)


def handle_save_btn():
    case = _get_selected_case()
    case_path_field_text = SharedState.m_widget.case_path_field.text_edit.text()
    case.cases_dir.path = Path(case_path_field_text)

    cam_prop = _get_selected_cam_prop()
    # slice_ = _get_selected_slice_prop()

    cam_form = SharedState.m_widget.camera_props_params_form
    cam_prop.cam_position = deepcopy(cam_form.position)
    cam_prop.viewup = deepcopy(cam_form.view_up)
    cam_prop.focal_point = deepcopy(cam_form.focal_point)
    cam_prop.viewangle = float(cam_form.view_angle)

    # slice_form = SharedState.m_widget.slice_params_form
    # if slice_form.x_slice_field.text_edit1.text() == "" \
    #         or slice_form.x_slice_field.text_edit2.text() == "" \
    #         or slice_form.x_slice_field.text_edit3.text() == "":
    #     slice_.sl_x = None
    # else:
    #     slice_.sl_x = slice_form.x_slice
    #
    # if slice_form.y_slice_field.text_edit1.text() == "" \
    #         or slice_form.y_slice_field.text_edit2.text() == "" \
    #         or slice_form.y_slice_field.text_edit3.text() == "":
    #     slice_.sl_y = None
    # else:
    #     slice_.sl_y = slice_form.y_slice
    #
    # if slice_form.z_slice_field.text_edit1.text() == "" \
    #         or slice_form.z_slice_field.text_edit2.text() == "" \
    #         or slice_form.z_slice_field.text_edit3.text() == "":
    #     slice_.sl_z = None
    # else:
    #     slice_.sl_z = slice_form.z_slice


def handle_reset_btn():
    case_dtos = MongoDaoFactory().get_dao(MongoFoamCaseDAO).get_all()
    cases = list(map(Mapper.map_foam_case_dto, case_dtos))
    SharedState.case_list = cases
    list_ = SharedState.m_widget.cases_control_list.list_
    list_.clear()
    list_.addItems([case.name for case in cases])
    if len(cases) > 0:
        list_.setCurrentRow(0)


def handle_save_db_btn():
    cases = SharedState.case_list
    for case in cases:
        handle_save_btn()
        MongoDaoFactory().get_dao(MongoFoamCaseDAO).create_or_update(Mapper.map_foam_case_to_dto(case))

    for case in SharedState.cases_for_del:
        MongoDaoFactory().get_dao(MongoFoamCaseDAO).delete(str(case.idn))

    for cam_prop in SharedState.cam_props_for_del:
        MongoDaoFactory().get_dao(MongoCameraPropsDAO).delete(str(cam_prop.idn))

    for sl in SharedState.slices_for_del:
        MongoDaoFactory().get_dao(MongoCameraSliceDAO).delete(str(sl.idn))

    SharedState.cam_props_for_del = []
    SharedState.slices_for_del = []
    SharedState.cases_for_del = []


def _get_selected_case_row():
    selected_item = SharedState.m_widget.cases_control_list.list_.selectedItems()[0]
    return SharedState.m_widget.cases_control_list.list_.row(selected_item)


def _get_selected_case():
    row = _get_selected_case_row()
    return SharedState.case_list[row]


def _get_selected_cam_prop_row():
    selected_item = SharedState.m_widget.camera_props_control_list.list_.selectedItems()
    if not selected_item:
        return None
    return SharedState.m_widget.camera_props_control_list.list_.row(selected_item[0])


def _get_selected_cam_prop():
    case = _get_selected_case()
    cam_row = _get_selected_cam_prop_row()
    return None if cam_row is None else case.cam_prop_list[cam_row]


def _get_selected_slice_prop_row():
    selected_item = SharedState.m_widget.slice_props_control_list.list_.selectedItems()
    if not selected_item:
        return None
    return SharedState.m_widget.slice_props_control_list.list_.row(selected_item[0])


def _get_selected_slice_prop():
    case = _get_selected_case()
    row = _get_selected_slice_prop_row()
    return None if row is None else case.slice_list[row]


handlers = {
    "handle_cases_add_button_clicked": handle_cases_add_button_clicked,
    "handle_cases_rm_button_clicked": handle_cases_rm_button_clicked,
    "handle_cases_item_selection": handle_cases_item_selection,
    "handle_generate_button_clicked": handle_generate_button_clicked,
    "handle_case_path_field_on_text_changed": handle_case_path_field_on_text_changed,
    "handle_camera_props_add_button_clicked": handle_camera_props_add_button_clicked,
    "handle_camera_props_rm_button_clicked": handle_camera_props_rm_button_clicked,
    "handle_camera_props_item_selection": handle_camera_props_item_selection,
    "handle_slice_props_add_button_clicked": handle_slice_props_add_button_clicked,
    "handle_slice_props_rm_button_clicked": handle_slice_props_rm_button_clicked,
    "handle_slice_props_item_selection": handle_slice_props_item_selection,
    "handle_save_btn": handle_save_btn,
    "handle_reset_btn": handle_reset_btn,
    "handle_save_db_btn": handle_save_db_btn
}

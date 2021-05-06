from pathlib import Path
from typing import List


class Point:
    def __init__(self, x: float, y: float, z: float):
        self._x = x
        self._y = y
        self._z = z

    def __repr__(self):
        return f"<Point: {self._x} {self._y} {self._z}>"

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z


class CameraProps:
    def __init__(self, idn: int, focal_point: Point, cam_position: Point, viewangle: int, viewup: Point, pp: bool):
        self._idn = idn
        self._focal_point = focal_point
        self._cam_position = cam_position
        self._viewup = viewup
        self._viewangle = viewangle
        self._parallel_projection = pp

    @property
    def idn(self) -> int:
        return self._idn

    @property
    def focal_point(self) -> Point:
        return self._focal_point

    @property
    def cam_position(self) -> Point:
        return self._cam_position

    @property
    def viewup(self) -> Point:
        return self._viewup

    @property
    def viewangle(self):
        return self._viewangle


class CameraSlice(object):
    def __init__(self, idn, sl_x: Point = None, sl_y: Point = None, sl_z: Point = None):
        self._idn = idn
        self._sl_x = sl_x
        self._sl_y = sl_y
        self._sl_z = sl_z

    @property
    def idn(self):
        return self._idn

    @property
    def sl_x(self):
        return self._sl_x

    @property
    def sl_y(self):
        return self._sl_y

    @property
    def sl_z(self):
        return self._sl_z


class CaseDir(object):
    def __init__(self, idn: int, path: str):
        self._idn = idn
        self._path = Path(path)

    @property
    def idn(self):
        return self._idn

    @property
    def path(self):
        return self._path


class FoamCase(object):
    def __init__(self, idn: int, case_dir: CaseDir, cam_prop_list: List[CameraProps], slice_list: List[CameraSlice]):
        self._idn = idn
        self._cases_dir = case_dir
        self._cam_prop_list = cam_prop_list
        self._slice_list = slice_list

    @property
    def idn(self) -> int:
        return self._idn

    @property
    def case_dir(self) -> CaseDir:
        return self._cases_dir

    @property
    def cam_prop_list(self) -> List[CameraProps]:
        return self._cam_prop_list

    @property
    def slice_list(self) -> List[CameraSlice]:
        return self._slice_list

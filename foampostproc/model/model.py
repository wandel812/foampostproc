from pathlib import Path
from typing import List


class Point:
    def __init__(self, x: int, y: int, z: int):
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
    def __init__(self, idn: int, focal_point: Point, cam_position: Point, angles: Point):
        self._idn = idn
        self._focal_point = focal_point
        self._cam_position = cam_position
        self._angles = angles

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
    def angels(self) -> Point:
        return self._angles


class CameraSlice(object):
    def __init__(self, cam_prop_id: int, sl: Point):
        self._cam_prop_id = cam_prop_id
        self._sl = sl

    @property
    def cam_prop_id(self) -> int:
        return self._cam_prop_id

    @property
    def sl(self):
        return self._sl


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
    def __init__(self, idn: int, cases_dir_path: CaseDir, cam_prop_list: List[CameraProps], slice_list: List[CameraSlice]):
        self._idn = idn
        self._cases_dir_path = cases_dir_path
        self._cam_prop_list = cam_prop_list
        self._slice_list = slice_list

    @property
    def idn(self) -> int:
        return self._idn

    @property
    def cases_dir_path(self) -> CaseDir:
        return self._cases_dir_path

    @property
    def cam_prop_list(self) -> List[CameraProps]:
        return self._cam_prop_list

    @property
    def slice_list(self) -> List[CameraSlice]:
        return self._slice_list

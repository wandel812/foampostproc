from abc import ABC, abstractmethod
from pathlib import Path
from typing import List


class Point:
    def __init__(self, x:int, y:int, z:int):
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
    def __init__(self, id_: int, focal_point: Point, cam_position: Point, angles: Point):
        self._id = id_
        self._focal_point = focal_point
        self._cam_position = cam_position
        self._angles = angles

    @property
    def id_(self) -> int:
        return self._id

    @property
    def focal_point(self) -> Point:
        return self._focal_point

    @property
    def cam_position(self) -> Point:
        return self._cam_position

    @property
    def angels(self) -> Point:
        return self._angles


class CameraSlice:
    def __int__(self, cam_prop_id: int, slice_: Point):
        self._cam_prop_id = cam_prop_id
        self._slice = slice_

    @property
    def cam_prop_id(self) -> int:
        return self._cam_prop_id

    @property
    def slice_(self):
        return self.slice_


class ICaseLike(ABC):
    @abstractmethod
    @property
    def case_path(self) -> Path: pass

    @abstractmethod
    @property
    def cam_prop_list(self) -> List[CameraProps]: pass

    @abstractmethod
    @property
    def slice_list(self) -> List[CameraSlice]: pass


class FoamCase(ICaseLike):
    def __init__(self, case_path: Path, cam_prop_list: List[CameraProps], slice_list: List[CameraSlice]):
        self._case_path = case_path
        self._cam_prop_list = cam_prop_list
        self._slice_list = slice_list

    @property
    def case_path(self) -> Path:
        return self._case_path

    @property
    def cam_prop_list(self) -> List[CameraProps]:
        return self._cam_prop_list

    @property
    def slice_list(self) -> List[CameraSlice]:
        return self._slice_list




from typing import NamedTuple, List


class FoamCasePathDTO:
    def __init__(self, case_path: str):
        self._case_path: str = case_path

    @property
    def case_path(self):
        return self._case_path


class PointDTO(NamedTuple):
    x: int
    y: int
    z: int


class CameraPropsDTO:
    def __init__(self, id_: int, focal_point: PointDTO, cam_position: PointDTO, angles: PointDTO):
        self._id = id_
        self._focal_point = focal_point
        self._cam_position = cam_position
        self._angles = angles

    @property
    def id_(self) -> int:
        return self._id

    @property
    def focal_point(self) -> PointDTO:
        return self._focal_point

    @property
    def cam_position(self) -> PointDTO:
        return self._cam_position

    @property
    def angels(self) -> PointDTO:
        return self._angles


class SliceDTO:
    def __int__(self, cam_prop_id: int, slice_: PointDTO):
        self._cam_prop_id = cam_prop_id
        self._slice = slice_

    @property
    def cam_prop_id(self) -> int:
        return self._cam_prop_id

    @property
    def slice_(self) -> PointDTO:
        return self.slice_





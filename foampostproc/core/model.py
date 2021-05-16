from pathlib import Path
from typing import List


class Point:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"<Point: {self.x} {self.y} {self.z}>"


class CameraProps:
    def __init__(self, idn, name: str, focal_point: Point, cam_position: Point, viewangle: int, viewup: Point):
        self.idn = idn
        self.name = name
        self.focal_point = focal_point
        self.cam_position = cam_position
        self.viewup = viewup
        self.viewangle = viewangle


class CameraSlice(object):
    def __init__(self, idn, name: str, sl_x: Point = None, sl_y: Point = None, sl_z: Point = None):
        self.idn = idn
        self.name = name
        self.sl_x = sl_x
        self.sl_y = sl_y
        self.sl_z = sl_z


class CasesDir(object):
    def __init__(self, idn, path: str):
        self.idn = idn
        self.path = Path(path)


class FoamCase(object):
    def __init__(self, idn, name: str, case_dir: CasesDir, cam_prop_list: List[CameraProps],
                 slice_list: List[CameraSlice]):
        self.idn = idn
        self.name = name
        self.cases_dir = case_dir
        self.cam_prop_list = cam_prop_list
        self.slice_list = slice_list

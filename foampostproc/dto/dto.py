from typing import List, Dict, Optional

from bson import ObjectId


class FoamCaseDTO(object):
    def __init__(self, cases_dir: 'CasesDirDTO', camera_props: List['CameraPropsDTO'],
                 camera_slices: List['SliceDTO'], _id=None, images: List[str] = None):
        if _id is None:
            _id = ObjectId()
        self._id = _id
        self.cases_dir = cases_dir
        self.camera_props = camera_props
        self.camera_slices = camera_slices
        self.images = images

    @staticmethod
    def parse(d: Dict):
        try:
            res = FoamCaseDTO(**d)
        except Exception:
            res = None
        return res


class CasesDirDTO(object):
    def __init__(self, cases_path: str, _id=None):
        if _id is None:
            _id = ObjectId()
        self._id = _id
        self.cases_path = cases_path

    @staticmethod
    def parse(d: Dict) -> Optional['CasesDirDTO']:
        try:
            res = CasesDirDTO(**d)
        except Exception:
            res = None
        return res


class PointDTO(object):
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    @staticmethod
    def parse(d: Dict) -> Optional['PointDTO']:
        try:
            res = PointDTO(**d)
        except Exception:
            res = None
        return res


class CameraPropsDTO(object):
    def __init__(self, focal_point: PointDTO, cam_position: PointDTO, viewangle: int, viewup: PointDTO,
                 _id=None):
        if _id is None:
            _id = ObjectId()
        self._id = _id
        self.focal_point = focal_point
        self.cam_position = cam_position
        self.viewangle = viewangle
        self.viewup = viewup

    @staticmethod
    def parse(d: Dict) -> Optional['CameraPropsDTO']:
        try:
            res = CameraPropsDTO(**d)
        except Exception:
            res = None
        return res


class SliceDTO(object):
    def __init__(self, sl_x: PointDTO = None, sl_y: PointDTO = None, sl_z: PointDTO = None, _id=None):
        if _id is None:
            _id = ObjectId()
        self._id = _id
        self.sl_x = sl_x
        self.sl_y = sl_y
        self.sl_z = sl_z

    @staticmethod
    def parse(d: Dict) -> Optional['SliceDTO']:
        try:
            res = SliceDTO(**d)
        except Exception:
            res = None
        return res


parse_functions = [FoamCaseDTO.parse, CasesDirDTO.parse, PointDTO.parse, CameraPropsDTO.parse, SliceDTO.parse]

def parse_config_json_hook(dct: Dict):
    res = None
    for parse in parse_functions:
        res = parse(dct)
        if res is not None:
            break

    if res is None:
        raise RuntimeError("Can't parse config file")

    return res

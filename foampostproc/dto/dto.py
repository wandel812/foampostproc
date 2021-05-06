from typing import List, Dict, Optional


class FoamCaseDTO(object):
    def __init__(self, idn: int, cases_dir: 'FoamCasesPathDTO', camera_props: List['CameraPropsDTO'],
                 sls: List['SliceDTO']):
        self.idn = idn
        self.cases_dir = cases_dir
        self.camera_props = camera_props
        self.sls = sls

    @staticmethod
    def parse(d: Dict):
        try:
            res = FoamCaseDTO(**d)
        except Exception:
            res = None
        return res


class FoamCasesPathDTO(object):
    def __init__(self, idn: int, case_path: str):
        self.idn = idn
        self.case_path = case_path

    @staticmethod
    def parse(d: Dict) -> Optional['FoamCasesPathDTO']:
        try:
            res = FoamCasesPathDTO(**d)
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
    def __init__(self, idn: int, focal_point: PointDTO, cam_position: PointDTO, viewangle: int, viewup: PointDTO,
                 pp: bool):
        self.idn = idn
        self.focal_point = focal_point
        self.cam_position = cam_position
        self.viewangle = viewangle
        self.viewup = viewup
        self.pp = pp

    @staticmethod
    def parse(d: Dict) -> Optional['CameraPropsDTO']:
        try:
            res = CameraPropsDTO(**d)
        except Exception:
            res = None
        return res


class SliceDTO(object):
    def __init__(self, idn: int, sl_x: PointDTO = None, sl_y: PointDTO = None, sl_z: PointDTO = None):
        self.idn = idn
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


parse_functions = [FoamCaseDTO.parse, FoamCasesPathDTO.parse, PointDTO.parse, CameraPropsDTO.parse, SliceDTO.parse]

def parse_config_json_hook(dct: Dict):
    res = None
    for parse in parse_functions:
        res = parse(dct)
        if res is not None:
            break

    if res is None:
        raise RuntimeError("Can't parse config file")

    return res


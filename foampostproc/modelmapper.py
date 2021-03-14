from pathlib import Path

from foampostproc.dto import FoamCasePathDTO, PointDTO, SliceDTO, CameraPropsDTO
from foampostproc.model import Point, CameraSlice, CameraProps


class Mapper:
    @classmethod
    def map_foam_case_path_dto(cls, foamcasepathdto: FoamCasePathDTO) -> Path:
        return Path(foamcasepathdto.case_path)

    @classmethod
    def map_point(cls, p: PointDTO) -> Point:
        return Point(p.x, p.y, p.z)

    @classmethod
    def map_slice(cls, s: SliceDTO) -> CameraSlice:
        return CameraSlice(s.cam_prop_id, cls.map_point(s.slice_))

    @classmethod
    def map_camera_props(cls, c: CameraPropsDTO) -> CameraProps:
        return CameraProps(c.id_, c.focal_point, c.cam_position, c.angels)

from foampostproc.dto.dto import CasesDirDTO, PointDTO, SliceDTO, CameraPropsDTO, FoamCaseDTO
from foampostproc.core.model.model import Point, CameraSlice, CameraProps, FoamCase, CasesDir


class Mapper:
    @classmethod
    def map_foam_case_dto(cls, foam_case: FoamCaseDTO):
        cam_props = [cls.map_camera_props_dto(cam_prop) for cam_prop in foam_case.camera_props]
        slices_ = []
        for sl in foam_case.camera_slices:
            t = cls.map_slice_dto(sl)
            slices_.append(t)

        #slices = [cls.map_slice_dto(sl) for sl in foam_case.slices]
        return FoamCase(foam_case._id, cls.map_foam_cases_path_dto(foam_case.cases_dir), cam_props, slices_)

    @classmethod
    def map_foam_cases_path_dto(cls, foam_cases_path_dto: CasesDirDTO) -> CasesDir:
        return CasesDir(foam_cases_path_dto._id, foam_cases_path_dto.cases_path)

    @classmethod
    def map_point_dto(cls, p: PointDTO) -> Point:
        return Point(p.x, p.y, p.z)

    @classmethod
    def map_slice_dto(cls, s: SliceDTO) -> CameraSlice:
        sl_x = None if s.sl_x is None else cls.map_point_dto(s.sl_x)
        sl_y = None if s.sl_y is None else cls.map_point_dto(s.sl_y)
        sl_z = None if s.sl_z is None else cls.map_point_dto(s.sl_z)
        return CameraSlice(s._id, sl_x, sl_y, sl_z)

    @classmethod
    def map_camera_props_dto(cls, c: CameraPropsDTO) -> CameraProps:
        return CameraProps(c. _id,
                           cls.map_point_dto(c.focal_point),
                           cls.map_point_dto(c.cam_position),
                           c.viewangle,
                           cls.map_point_dto(c.viewup))

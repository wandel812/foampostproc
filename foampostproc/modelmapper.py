from foampostproc.dto.dto import FoamCasesPathDTO, PointDTO, SliceDTO, CameraPropsDTO, FoamCaseDTO
from foampostproc.model.model import Point, CameraSlice, CameraProps, FoamCase, CaseDir


class Mapper:
    @classmethod
    def map_foam_case_dto(cls, foam_case: FoamCaseDTO):
        cam_props = [cls.map_camera_props_dto(cam_prop) for cam_prop in foam_case.camera_props]
        slices_ = []
        for sl in foam_case.sls:
            t = cls.map_slice_dto(sl)
            slices_.append(t)

        #slices = [cls.map_slice_dto(sl) for sl in foam_case.slices]
        return FoamCase(foam_case.idn, cls.map_foam_cases_path_dto(foam_case.cases_dir), cam_props, slices_)

    @classmethod
    def map_foam_cases_path_dto(cls, foam_cases_path_dto: FoamCasesPathDTO) -> CaseDir:
        return CaseDir(foam_cases_path_dto.idn, foam_cases_path_dto.case_path)

    @classmethod
    def map_point_dto(cls, p: PointDTO) -> Point:
        return Point(p.x, p.y, p.z)

    @classmethod
    def map_slice_dto(cls, s: SliceDTO) -> CameraSlice:
        return CameraSlice(s.idn, cls.map_point_dto(s.sl))

    @classmethod
    def map_camera_props_dto(cls, c: CameraPropsDTO) -> CameraProps:
        return CameraProps(c. idn,
                           cls.map_point_dto(c.focal_point),
                           cls.map_point_dto(c.cam_position),
                           c.viewangle,
                           cls.map_point_dto(c.viewup),
                           c.pp)

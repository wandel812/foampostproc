from foampostproc.dto.dto import CasesDirDTO, PointDTO, SliceDTO, CameraPropsDTO, FoamCaseDTO
from foampostproc.core.model import Point, CameraSlice, CameraProps, FoamCase, CasesDir


class Mapper:
    @classmethod
    def map_foam_case_dto(cls, foam_case: FoamCaseDTO) -> FoamCase:
        cam_props = [cls.map_camera_props_dto(cam_prop) for cam_prop in foam_case.camera_props]
        slices_ = []
        for sl in foam_case.camera_slices:
            t = cls.map_slice_dto(sl)
            slices_.append(t)

        return FoamCase(foam_case._id,
                        foam_case.name,
                        cls.map_foam_cases_path_dto(foam_case.cases_dir),
                        cam_props,
                        slices_)

    @classmethod
    def map_foam_case_to_dto(cls, foam_case: FoamCase) -> FoamCaseDTO:
        cam_prop_dtos = [cls.map_camera_props_to_dto(cam_prop)
                         for cam_prop in foam_case.cam_prop_list]
        slice_dtos = []
        for sl in foam_case.slice_list:
            t = cls.map_slice_to_dto(sl)
            slice_dtos.append(t)
        cases_path = cls.map_foam_cases_path_to_dto(foam_case.cases_dir)

        return FoamCaseDTO(cases_path,
                           cam_prop_dtos,
                           slice_dtos,
                           foam_case.name,
                           _id=foam_case.idn)

    @classmethod
    def map_foam_cases_path_dto(cls, foam_cases_path_dto: CasesDirDTO) -> CasesDir:
        return CasesDir(foam_cases_path_dto._id, foam_cases_path_dto.cases_path)

    @classmethod
    def map_foam_cases_path_to_dto(cls, foam_cases_path: CasesDir) -> CasesDirDTO:
        return CasesDirDTO(str(foam_cases_path.path), _id=foam_cases_path.idn)

    @classmethod
    def map_point_dto(cls, p_dto) -> Point:
        if isinstance(p_dto, PointDTO):
            return Point(p_dto.x, p_dto.y, p_dto.z)
        else:
            return Point(p_dto["x"], p_dto["y"], p_dto["z"])

    @classmethod
    def map_point_to_dto(cls, p: Point) -> PointDTO:
        return PointDTO(p.x, p.y, p.z)

    @classmethod
    def map_slice_dto(cls, s_dto: SliceDTO) -> CameraSlice:
        sl_x = None if s_dto.sl_x is None else cls.map_point_dto(s_dto.sl_x)
        sl_y = None if s_dto.sl_y is None else cls.map_point_dto(s_dto.sl_y)
        sl_z = None if s_dto.sl_z is None else cls.map_point_dto(s_dto.sl_z)
        return CameraSlice(s_dto._id, s_dto.name, sl_x, sl_y, sl_z)

    @classmethod
    def map_slice_to_dto(cls, s: CameraSlice) -> SliceDTO:
        sl_x = None if s.sl_x is None else cls.map_point_to_dto(s.sl_x)
        sl_y = None if s.sl_y is None else cls.map_point_to_dto(s.sl_y)
        sl_z = None if s.sl_z is None else cls.map_point_to_dto(s.sl_z)
        return SliceDTO(s.name, sl_x, sl_y, sl_z, _id=s.idn)

    @classmethod
    def map_camera_props_dto(cls, c_dto: CameraPropsDTO) -> CameraProps:
        return CameraProps(c_dto._id,
                           c_dto.name,
                           cls.map_point_dto(c_dto.focal_point),
                           cls.map_point_dto(c_dto.cam_position),
                           c_dto.viewangle,
                           cls.map_point_dto(c_dto.viewup))

    @classmethod
    def map_camera_props_to_dto(cls, c: CameraProps) -> CameraPropsDTO:
        focal_point_dto = cls.map_point_to_dto(c.focal_point)
        cam_position_dto = cls.map_point_to_dto(c.cam_position)
        viewup = cls.map_point_to_dto(c.viewup)
        return CameraPropsDTO(focal_point_dto, cam_position_dto,
                              c.viewangle, viewup, c.name, _id=c.idn)

from os.path import dirname, abspath
from pathlib import Path
from paraview.simple import *

import foampostproc.dto.dto as dto
from foampostproc.file import FileHandling
from modelmapper import Mapper

# TODO ADD SLICE TYPE ??
# https://docs.paraview.org/en/v5.8.1/UsersGuide/displayingData.html?highlight=slice#slice-view

SRC_DIR = Path(dirname(abspath(__file__)))
PROJ_DIR = SRC_DIR.parent
OTP_DIR = PROJ_DIR / "otp"

if __name__ == "__main__":
    case_dto = FileHandling.read_json(PROJ_DIR / "config/conf.json",
                                      object_hook_=dto.parse_config_json_hook)

    case = Mapper.map_foam_case_dto(case_dto)

    foamcase_path = case.cases_dir_path.path
    foamcase = FileHandling.read_foamcase(foamcase_path)
    foamcase.MeshRegions = ['internalMesh']
    servermanager.Fetch(foamcase)
    view = CreateRenderView(foamcase)
    view.ViewTime = max(foamcase.TimestepValues)
    for i, cam_prop in enumerate(case.cam_prop_list):
        camera = view.GetActiveCamera()
        camera.SetFocalPoint(cam_prop.focal_point.x, cam_prop.focal_point.y, cam_prop.focal_point.z)
        camera.SetPosition(cam_prop.cam_position.x, cam_prop.cam_position.y, cam_prop.cam_position.z)
        camera.SetViewUp(cam_prop.viewup.x, cam_prop.viewup.y, cam_prop.viewup.z)
        camera.SetParallelProjection(cam_prop.parallel_projection)
        for j, sl in enumerate(case.slice_list):
            Show(foamcase, view)
            # Render(view)
            SaveScreenshot(str(OTP_DIR / f"view-{i}-{j}.png"), view)

from os.path import dirname, abspath
from pathlib import Path
from paraview.simple import *

import foampostproc.dto.dto as dto
from foampostproc.file import FileHandling
from modelmapper import Mapper

SRC_DIR = Path(dirname(abspath(__file__)))
PROJ_DIR = SRC_DIR.parent

if __name__ == "__main__":
    case_dto = FileHandling.read_json(PROJ_DIR / "config/conf.json",
                                      object_hook_=dto.parse_config_json_hook)

    case = Mapper.map_foam_case_dto(case_dto)

    #foamcase_path = Path("/home/dm/openfoam/case0")
    foamcase_path = case.cases_dir_path.path
    foamcase = FileHandling.read_foamcase(foamcase_path)
    foamcase.MeshRegions = ['internalMesh']
    servermanager.Fetch(foamcase)
    view = CreateRenderView(foamcase)
    view.ViewTime = max(foamcase.TimestepValues)
    Show(foamcase, view)
    # Render(view)
    SaveScreenshot("aview.png", view)

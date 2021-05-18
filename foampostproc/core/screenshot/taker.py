from pathlib import Path
from glob import glob
from paraview.simple import *

from foampostproc.utils import FileHandling


class Screenshot:
    @classmethod
    def take_screenshots(cls, foam_case_list, out: Path):
        for i, foam_case in enumerate(foam_case_list):
            cases = glob(str(foam_case.cases_dir.path / "*/"))
            for case in cases:
                foamcase_path = Path(case)
                foamcase = FileHandling.read_foamcase(foamcase_path)
                foamcase.MeshRegions = ['internalMesh']
                servermanager.Fetch(foamcase)
                view = CreateRenderView(foamcase)
                print(foamcase.TimestepValues)
                view.ViewTime = max(foamcase.TimestepValues)
                for j, cam_prop in enumerate(foam_case.cam_prop_list):
                    camera = view.GetActiveCamera()
                    camera.SetFocalPoint(cam_prop.focal_point.x, cam_prop.focal_point.y,
                                         cam_prop.focal_point.z)
                    camera.SetPosition(cam_prop.cam_position.x, cam_prop.cam_position.y,
                                       cam_prop.cam_position.z)
                    camera.SetViewUp(cam_prop.viewup.x, cam_prop.viewup.y,
                                     cam_prop.viewup.z)
                    camera.SetViewAngle(cam_prop.viewangle)

                    display = Show(foamcase, view)
                    ColorBy(display, ('POINTS', 'U'))
                    display.RescaleTransferFunctionToDataRange(True)
                    SaveScreenshot(str(out / f"view-{foamcase_path.name}-{i}-{j}.png"),
                                   view)

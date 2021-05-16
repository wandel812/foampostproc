from os.path import dirname, abspath
from pathlib import Path
from typing import Any
from ntpath import split
from os import makedirs
from json import dumps, load
from paraview.simple import *

SRC_DIR = Path(dirname(abspath(__file__)))
PROJ_DIR = SRC_DIR.parent


class SharedState(object):
    case_list = []
    m_widget = None
    cam_props_for_del = []
    slices_for_del = []
    cases_for_del = []


class FileHandling(object):
    @classmethod
    def write_json(cls, obj, path: str) -> None:
        def get_object_dict(d):
            return d.__dict__

        filepath, _ = split(path)
        if filepath:
            makedirs(filepath, exist_ok=True)
        with open(path, "w") as out:
            json_string = dumps(obj, default=get_object_dict)
            out.write(json_string)

    @classmethod
    def read_json(cls, inp: Path, object_hook_=None) -> Any:
        with open(inp, "r") as fin:
            data = load(fin, object_hook=object_hook_)

        return data

    @classmethod
    def read_foamcase(cls, inp: Path):
        foamcase_path = inp / "temp.foam"
        cls.write_file(foamcase_path)
        foamcase = OpenFOAMReader(FileName=str(foamcase_path))
        Path.unlink(foamcase_path)
        return foamcase

    @classmethod
    def write_file(cls, file_path: Path, text: str = "", mode: str = 'w'):
        dir_path = file_path.parent
        dir_path.mkdir(parents=True, exist_ok=True)
        with open(file_path, mode) as out:
            out.write(text)


if __name__ == "__main__":
    print(PROJ_DIR)

from collections import Callable
from pathlib import Path
from plistlib import Dict
from typing import Any
from ntpath import split
from os import makedirs
from json import dumps


class FileHandling:
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
    def read_json(cls, inp: Path, object_hook_: Callable[[Dict], Any]) -> Any:
        from json import load

        with open(inp, "r") as fin:
            data = load(fin, object_hook=object_hook_)

        return data

    @classmethod
    def write_file(cls, file_path: Path, text: str, mode: str = 'w'):
        dir_path = file_path.parent
        dir_path.mkdir(parents=True, exist_ok=True)
        with open(file_path, mode) as out:
            out.write(text)
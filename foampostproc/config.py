import configparser
from pathlib import Path
from typing import List

# gui generator config -------------------------------------------------------------------------------------------------
from foampostproc.utils import PROJ_DIR

CONFIG_PATH = PROJ_DIR / Path("config/app.ini")


class Config:
    __config: configparser.RawConfigParser = configparser.ConfigParser()
    __is_read = False

    @classmethod
    def get_section(cls, section: str) -> 'ConfigSectionProxy':
        if not cls.__is_read:
            cls._read_config()
        return ConfigSectionProxy(cls.__config[section])

    @classmethod
    def _read_config(cls):
        cls.__config.read(CONFIG_PATH)
        cls.__is_read = True


class ConfigSectionProxy:
    COMMON_SECTION: str = "Common"
    USE_PROJ_PREFIX_FOR_PATHS = "use_proj_prefix_for_paths"

    __raw_config: configparser.RawConfigParser = configparser.ConfigParser()
    __raw_config.read(CONFIG_PATH)
    _common_section_config = __raw_config[COMMON_SECTION]

    def __init__(self, section_proxy: configparser.SectionProxy):
        self.__section_proxy = section_proxy

    def get_int(self, option: str) -> int:
        return self.__section_proxy.getint(option)

    def get_float(self, option: str) -> float:
        return self.__section_proxy.getfloat(option)

    def get_boolean(self, option: str) -> bool:
        return self.__section_proxy.getboolean(option)

    def get(self, option: str) -> str:
        return self.__section_proxy.get(option)

    def get_path(self, option: str) -> Path:
        option_path = Path(self.__section_proxy.get(option))
        use_prefix = self._common_section_config.getboolean(self.USE_PROJ_PREFIX_FOR_PATHS)
        return Path(PROJ_DIR) / option_path if use_prefix else option_path

    def get_list(self, option: str) -> List[str]:
        return list(map(lambda s: s.strip(), self.get(option).split(',')))

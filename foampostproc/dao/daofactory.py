from abc import ABC, abstractmethod
from pymongo import MongoClient

from foampostproc.config import Config


class DaoFactory(ABC):
    @abstractmethod
    def _get_connection(self):
        pass

    @abstractmethod
    def get_dao(self, connection, dao_class):
        pass


class MongoDaoFactory(DaoFactory):
    LOGIN = Config.get_section("DataBaseUser").get("login")
    PASSWORD = Config.get_section("DataBaseUser").get("password")
    DB_PROJ_NAME = Config.get_section("DataBaseUser").get("db_proj_name")
    DB_CONNECT_LINK = f"mongodb+srv://{LOGIN}:{PASSWORD}@cluster0.ecqqe.mongodb.net/" \
                      f"{DB_PROJ_NAME}?retryWrites=true&w=majority"

    def _get_connection(self):
        cluster = MongoClient(self.DB_CONNECT_LINK)
        return cluster.foampostproc_db

    map_collection = {
        "MongoFoamCaseDAO": "foamcase",
        "MongoCaseDirDAO": "casesdir",
        "MongoCameraSliceDAO": "cameraslice",
        "MongoCameraPropsDAO": "cameraprops"
    }

    def _get_collection(self, connection, dao_class):
        return connection[self.map_collection[dao_class.__name__]]

    def get_dao(self, dao_class, connection=None):
        if connection is None:
            connection = self._get_connection()
        collection = self._get_collection(connection, dao_class)
        return dao_class(collection)

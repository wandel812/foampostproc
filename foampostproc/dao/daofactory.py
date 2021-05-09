from abc import ABC, abstractmethod
from pymongo import MongoClient


class DaoFactory(ABC):
    @abstractmethod
    def get_connection(self):
        pass

    @abstractmethod
    def get_dao(self, connection, dto_class):
        pass


class MongoDaoFactory(DaoFactory):
    login = "dbUser"
    password = "a4eYAyhZ4xgXEre"
    db_proj_name = "foampostproc"

    def get_connection(self):
        db_connect_link = f"mongodb+srv://{self.login}:{self.password}@cluster0.ecqqe.mongodb.net/" \
                          f"{self.db_proj_name}?retryWrites=true&w=majority"
        cluster = MongoClient(db_connect_link)
        return cluster.foampostproc_db

    map_collection = {
        "MongoFoamCaseDAO": "foamcase",
        "MongoCaseDirDAO": "casesdir",
        "MongoCameraSliceDAO": "cameraslices",
        "MongoCameraPropsDAO": "cameraprops"
    }

    def _get_collection(self, connection, dao_class):
        return connection[self.map_collection[dao_class.__name__]]

    def get_dao(self, dao_class, connection=None):
        if connection is None:
            connection = self.get_connection()
        collection = self._get_collection(connection, dao_class)
        return dao_class(collection)

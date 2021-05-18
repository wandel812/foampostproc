from abc import ABC, abstractmethod
from typing import Any, List
from foampostproc.dao.daofactory import MongoDaoFactory
from foampostproc.dto.dto import FoamCaseDTO, CasesDirDTO, CameraPropsDTO, SliceDTO


class AbstractDAO(ABC):
    def __init__(self, collection_conn):
        self._connection = collection_conn

    @property
    def connection(self):
        return self._connection

    @abstractmethod
    def create(self, obj: Any) -> Any:
        pass

    def create_or_update(self, obj: Any) -> Any:
        pass

    @abstractmethod
    def read(self, key: str) -> Any:
        pass

    @abstractmethod
    def update(self, obj: Any):
        pass

    @abstractmethod
    def delete(self, key: str):
        pass

    @abstractmethod
    def get_all(self) -> List[Any]:
        pass


class MongoAbstractDAO(AbstractDAO, ABC):
    def delete(self, key: str) -> Any:
        try:
            self.connection.delete_one({"_id": key})
        except Exception:
            raise RuntimeError("Something went wrong with object deletion")

    def get_all(self) -> List[Any]:
        db_obj_list = self.connection.find()
        return [self.read(db_obj["_id"]) for db_obj in db_obj_list]


class MongoFoamCaseDAO(MongoAbstractDAO):
    def create(self, dto_obj: FoamCaseDTO):
        try:
            camera_props_ids = [str(prop._id) for prop in dto_obj.camera_props]
            camera_slices_ids = [str(sl._id) for sl in dto_obj.camera_slices]
            cases_dir_id = str(dto_obj.cases_dir._id)
            _id = str(dto_obj._id)

            if self.connection.count_documents({"_id": _id}) == 0:
                self.connection.insert_one({
                    "_id": _id,
                    "name": dto_obj.name,
                    "cases_dir": cases_dir_id,
                    "camera_props": camera_props_ids,
                    "camera_slices": camera_slices_ids
                })

            camera_props_dao = MongoDaoFactory().get_dao(MongoCameraPropsDAO)
            for dto_camera_prop in dto_obj.camera_props:
                camera_props_dao.create(dto_camera_prop)

            camera_slices_dao = MongoDaoFactory().get_dao(MongoCameraSliceDAO)
            for dto_camera_slice in dto_obj.camera_slices:
                camera_slices_dao.create(dto_camera_slice)

            MongoDaoFactory().get_dao(MongoCaseDirDAO).create(dto_obj.cases_dir)
            return self.connection.count_documents({"_id": _id}) == 0
        except Exception:
            raise RuntimeError("Something went wrong with object creation")

    def read(self, key: str) -> FoamCaseDTO:
        try:
            obj_dct = self.connection.find_one({"_id": key})
            dao_fact = MongoDaoFactory()
            cases_dir = dao_fact.get_dao(MongoCaseDirDAO).read(obj_dct["cases_dir"])
            camera_props = [dao_fact.get_dao(MongoCameraPropsDAO).read(prop)
                            for prop in obj_dct["camera_props"]]
            camera_slices = [dao_fact.get_dao(MongoCameraSliceDAO).read(sl)
                             for sl in obj_dct["camera_slices"]]
            return FoamCaseDTO(cases_dir, camera_props, camera_slices,
                               obj_dct["name"], obj_dct["_id"])
        except Exception:
            raise RuntimeError("Something went wrong with object reading")

    def update(self, dto_obj: FoamCaseDTO):
        try:
            camera_props_ids = [str(prop._id) for prop in dto_obj.camera_props]
            camera_slices_ids = [str(sl._id) for sl in dto_obj.camera_slices]
            cases_dir_id = str(dto_obj.cases_dir._id)
            print(camera_props_ids, dto_obj._id)
            self.connection.update_one({"_id": str(dto_obj._id)},
                                       {"$set": {
                                           "name": dto_obj.name,
                                           "cases_dir": cases_dir_id,
                                           "camera_props": camera_props_ids,
                                           "camera_slices": camera_slices_ids
                                       }})

            camera_props_dao = MongoDaoFactory().get_dao(MongoCameraPropsDAO)
            for dto_camera_prop in dto_obj.camera_props:
                camera_props_dao.create(dto_camera_prop)
            camera_slices_dao = MongoDaoFactory().get_dao(MongoCameraSliceDAO)
            for dto_camera_slice in dto_obj.camera_slices:
                camera_slices_dao.create(dto_camera_slice)
            MongoDaoFactory().get_dao(MongoCaseDirDAO).create(dto_obj.cases_dir)
        except Exception:
            raise RuntimeError("Something went wrong with object updating")

    def create_or_update(self, dto_obj: FoamCaseDTO):
        result = self.create(dto_obj)
        if not result:
            self.update(dto_obj)
            camera_props_dao = MongoDaoFactory().get_dao(MongoCameraPropsDAO)
            for dto_camera_prop in dto_obj.camera_props:
                camera_props_dao.create_or_update(dto_camera_prop)
            camera_slices_dao = MongoDaoFactory().get_dao(MongoCameraSliceDAO)
            for dto_camera_slice in dto_obj.camera_slices:
                camera_slices_dao.create(dto_camera_slice)
            MongoDaoFactory().get_dao(MongoCaseDirDAO) \
                .create_or_update(dto_obj.cases_dir)


class MongoCaseDirDAO(MongoAbstractDAO):
    def create(self, dto_obj: CasesDirDTO):
        try:
            if self.connection.count_documents({"_id": str(dto_obj._id)}) == 0:
                self.connection.insert_one({"_id": str(dto_obj._id),
                                            "cases_path": dto_obj.cases_path})
                return True
            return False
        except Exception:
            raise RuntimeError("Something went wrong with object creation")

    def read(self, key: str) -> CasesDirDTO:
        try:
            db_obj = self.connection.find_one({"_id": key})
            return CasesDirDTO(**db_obj)
        except Exception:
            raise RuntimeError("Something went wrong with object reading")

    def update(self, dto_obj: CasesDirDTO):
        try:
            self.connection.update_one({"_id": str(dto_obj._id)},
                                       {"$set": {
                                           "cases_path": dto_obj.cases_path
                                       }})
        except Exception:
            raise RuntimeError("Something went wrong with object updating")

    def create_or_update(self, dto_obj: CasesDirDTO):
        result = self.create(dto_obj)
        if not result:
            self.update(dto_obj)


class MongoCameraPropsDAO(MongoAbstractDAO):
    def create(self, dto_obj: CameraPropsDTO):
        try:
            if self.connection.count_documents({"_id": str(dto_obj._id)}) == 0:
                self.connection.insert_one({
                    "_id": str(dto_obj._id),
                    "name": dto_obj.name,
                    "focal_point": dto_obj.focal_point.__dict__,
                    "cam_position": dto_obj.cam_position.__dict__,
                    "viewangle": dto_obj.viewangle,
                    "viewup": dto_obj.viewup.__dict__,
                })
                return True
            return False
        except Exception:
            raise RuntimeError("Something went wrong with object creation")

    def read(self, key: str) -> CameraPropsDTO:
        try:
            db_obj = self.connection.find_one({"_id": key})
            return CameraPropsDTO(**db_obj)
        except Exception:
            raise RuntimeError("Something went wrong with object reading")

    def update(self, dto_obj: CameraPropsDTO):
        try:
            self.connection.update_one({"_id": str(dto_obj._id)},
                                       {"$set": {
                                           "name": dto_obj.name,
                                           "focal_point": dto_obj.focal_point.__dict__,
                                           "cam_position": dto_obj.cam_position.__dict__,
                                           "viewangle": dto_obj.viewangle,
                                           "viewup": dto_obj.viewup.__dict__
                                       }})
        except Exception:
            raise RuntimeError("Something went wrong with object updating")

    def create_or_update(self, dto_obj: CameraPropsDTO):
        result = self.create(dto_obj)
        if not result:
            self.update(dto_obj)


class MongoCameraSliceDAO(MongoAbstractDAO):
    def create(self, dto_obj: SliceDTO):
        try:
            if self.connection.count_documents({"_id": str(dto_obj._id)}) == 0:
                self.connection.insert_one({
                    "_id": str(dto_obj._id),
                    "name": dto_obj.name,
                    "sl_x": None if dto_obj.sl_x is None else dto_obj.sl_x.__dict__,
                    "sl_y": None if dto_obj.sl_y is None else dto_obj.sl_y.__dict__,
                    "sl_z": None if dto_obj.sl_z is None else dto_obj.sl_z.__dict__
                })
                return True
            return False
        except Exception:
            raise RuntimeError("Something went wrong with object creation")

    def read(self, key: str) -> SliceDTO:
        try:
            return SliceDTO(**self.connection.find_one({"_id": key}))
        except Exception:
            raise RuntimeError("Something went wrong with object reading")

    def update(self, dto_obj: SliceDTO):
        try:
            self.connection.update_one(
                {"_id": str(dto_obj._id)},
                {"$set": {
                    "name": dto_obj.name,
                    "sl_x": None if dto_obj.sl_x is None else dto_obj.sl_x.__dict__,
                    "sl_y": None if dto_obj.sl_y is None else dto_obj.sl_y.__dict__,
                    "sl_z": None if dto_obj.sl_z is None else dto_obj.sl_z.__dict__
                }})
        except Exception:
            raise RuntimeError("Something went wrong with object updating")

    def create_or_update(self, dto_obj: SliceDTO):
        result = self.create(dto_obj)
        if not result:
            self.update(dto_obj)

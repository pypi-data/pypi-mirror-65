from bson import CodecOptions
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.client_session import ClientSession
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.results import DeleteResult, InsertOneResult, UpdateResult

from .models import DocumentDBModel
from fa_common import get_current_app, get_timezone


class MongoDBClient(object):
    """
    Singleton client for interacting with MongoDB.
    Operates mostly using models, specified when making DB queries.

    Implements only part of internal `motor` methods, but can be populated more.

    Please don't use it directly, use `scidra.core.db.utils.get_db_client`.
    """

    __instance = None
    mongodb: AsyncIOMotorClient = None

    def __new__(cls) -> "MongoDBClient":
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            app = get_current_app()
            tzinfo = get_timezone()
            cls.__instance.codec_options = CodecOptions(tz_aware=True, tzinfo=tzinfo)
            cls.__instance.mongodb = app.mongodb
        return cls.__instance

    def get_collection(self, collection_name: str) -> Collection:
        return self.mongodb.get_collection(
            collection_name, codec_options=self.codec_options
        )

    async def insert(
        self,
        model: DocumentDBModel,
        session: ClientSession = None,
        include=None,
        exclude=None,
    ) -> InsertOneResult:
        data = model.dict(include=include, exclude=exclude)
        data["_id"] = data.pop("id")
        collection_name = model.get_db_collection()
        collection = self.get_collection(collection_name)
        return await collection.insert_one(data, session=session)

    async def count(
        self, model: DocumentDBModel, session: ClientSession = None, **kwargs
    ) -> int:
        _id = kwargs.pop("id", None)
        if _id is not None:
            kwargs["_id"] = _id

        collection_name = model.get_db_collection()
        collection = self.get_collection(collection_name)
        res = await collection.count_documents(kwargs, session=session)
        return res

    async def delete(
        self, model: DocumentDBModel, session: ClientSession = None, **kwargs
    ) -> DeleteResult:
        _id = kwargs.pop("id", None)
        if _id is not None:
            kwargs["_id"] = _id

        collection_name = model.get_db_collection()
        collection = self.get_collection(collection_name)
        res = await collection.delete_many(kwargs, session=session)
        return res

    async def update_one(
        self,
        model: DocumentDBModel,
        filter_kwargs: dict,
        session: ClientSession = None,
        **kwargs
    ) -> UpdateResult:
        _id = filter_kwargs.pop("id", None)
        if _id is not None:
            filter_kwargs["_id"] = _id

        collection_name = model.get_db_collection()
        collection = self.get_collection(collection_name)
        res = await collection.update_one(filter_kwargs, kwargs, session=session)
        return res

    async def update_many(
        self,
        model: DocumentDBModel,
        filter_kwargs: dict,
        session: ClientSession = None,
        **kwargs
    ) -> UpdateResult:
        _id = filter_kwargs.pop("id", None)
        if _id is not None:
            filter_kwargs["_id"] = _id

        collection_name = model.get_db_collection()
        collection = self.get_collection(collection_name)
        res = await collection.update_many(filter_kwargs, kwargs, session=session)
        return res

    async def get(
        self, model: DocumentDBModel, session: ClientSession = None, **kwargs
    ) -> dict:
        _id = kwargs.pop("id", None)
        if _id is not None:
            kwargs["_id"] = _id

        collection_name = model.get_db_collection()
        collection = self.get_collection(collection_name)
        res = await collection.find_one(kwargs, session=session)
        return res

    def list(
        self,
        model: DocumentDBModel,
        session: ClientSession = None,
        _offset: int = 0,
        _limit: int = 0,
        _sort: list = None,
        **kwargs
    ) -> Cursor:
        _id = kwargs.pop("id", None)
        if _id is not None:
            kwargs["_id"] = _id

        collection_name = model.get_db_collection()
        collection = self.get_collection(collection_name)
        return collection.find(
            kwargs, session=session, skip=_offset, limit=_limit, sort=_sort
        )

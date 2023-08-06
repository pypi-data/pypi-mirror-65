import logging

from functools import wraps
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorClient

from .document_dict import DocumentDict
from .document_array import DocumentArray

LOG = logging.getLogger("mdocument")


def check_setup(func):
    """Decorator for checking that document have valid loop and client."""

    async def arg_wrap(cls, *args, **kwargs):
        self = None
        if not isinstance(cls, type):
            self = cls
            cls = cls.__class__
        if "client" not in cls.__dict__:
            raise ClientNotFound()
        elif "database" not in cls.__dict__:
            raise DocumentException("Required attribute database is missing.")
        elif "collection" not in cls.__dict__:
            raise DocumentException("Required attribute collection is missing.")
        return await func(self, *args, **kwargs) if self else await func(cls, *args, **kwargs)

    return arg_wrap


class DocumentException(Exception):
    def __init__(self, message):
        self.message = message


class DocumentDoesntExist(DocumentException):
    def __init__(self):
        super().__init__("Document not found")


class ClientNotFound(DocumentException):
    def __init__(self):
        super().__init__("Client is not provided. Can't connect to database.")


class MetaDocument(type):
    database: str
    collection: str
    client: AsyncIOMotorClient
    collection: AsyncIOMotorCollection

    def _collection(cls) -> AsyncIOMotorCollection:
        for field in ("client", "database", "collection"):
            if field not in cls.__dict__:
                raise type("{}NotFound".format(field.capitalize()), (DocumentException,), {})(
                    f"Required attribute {field} is missing."
                )

        client = cls.__dict__["client"]
        database = cls.__dict__["database"]
        collection = cls.__dict__["collection"]

        return client[database][collection]

    def __getattribute__(cls, item: str):
        if item in ("database", "client"):
            raise AttributeError(item)
        elif item == "collection":
            return super().__getattribute__("_collection")
        return super().__getattribute__(item)


class Document(metaclass=MetaDocument):
    relations = {}

    def __init__(self, **kwargs):
        super().__setattr__("_document_", DocumentDict(kwargs))
        super().__setattr__("shadow_copy", DocumentDict(kwargs.copy()))

    def __repr__(self):
        return "{0}({1})".format(
            self.__class__.__name__,
            ", ".join(f"{key}={value}" for key, value in self._document_.items())
        )

    def __getattribute__(self, item):
        if item in ("collection", "database", "client"):
            if item in self._document_:
                return self._document_[item]
            raise AttributeError()
        return super().__getattribute__(item)

    def __getattr__(self, item, special=False):
        try:
            if isinstance(self._document_[item], dict):
                return DocumentDict(self._document_[item])
            elif isinstance(self._document_[item], list):
                return DocumentArray(self._document_[item])
            return self._document_[item]
        except KeyError:
            raise AttributeError(item)

    def __setattr__(self, key, value):
        self._document_[key] = value

    def __delattr__(self, item):
        del self._document_[item]

    def __setitem__(self, key, value):
        return setattr(self, key, value)

    def __getitem__(self, item):
        return self._document_[item]

    def __delitem__(self, key):
        return delattr(self, key)

    def __iter__(self):
        return iter(self._document_.items())

    async def _update_related(self):
        """Force updates related fields in other documents."""

        self_relations = set({v for v in self.__class__.__dict__.values()
                              if isinstance(v, property)})

        relate_properties = set(Document.relations).intersection(self_relations)

        if not relate_properties:
            return

        property_data = [Document.relations[relate] for relate in relate_properties]

        for prop in property_data:
            self_field = prop["self_field"]
            other_field = prop["other_field"]
            document = prop["other_document_func"]()
            if self[self_field] != self._shadow_copy_[self_field]:
                await document.collection.update_many(
                    {other_field: self._shadow_copy_[self_field]},
                    {"$set": {other_field: self[self_field]}}
                )

    @check_setup
    async def push_update(self):
        """Force update document."""

        await self._update_related()
        return await self.__class__._collection().replace_one(
            {"_id": self.shadow_copy._id}, self._document_)

    @classmethod
    @check_setup
    async def exists(cls, *args, **kwargs):
        """Checks that document exists."""

        if await cls._collection().find_one(*args, **kwargs):
            return True
        return False

    @classmethod
    @check_setup
    async def one(cls, **kwargs):
        """Finds one document based on kwargs."""

        document = await cls._collection().find_one(kwargs)
        if not document:
            raise DocumentDoesntExist()
        return cls(**document)

    @classmethod
    @check_setup
    async def many(cls, **kwargs) -> list:
        """Finds multiple documents based on kwargs."""

        result_list = []
        cursor = cls._collection().find(kwargs)
        async for doc in cursor:
            result_list.append(cls(**doc))
        return result_list

    @classmethod
    @check_setup
    async def create(cls, **kwargs) -> "Document":
        """Create new document."""

        await cls._collection().insert_one(kwargs)
        return cls(**kwargs)


    async def _delete_by_prop(self, relations):

        for prop, delete_info in relations.items():

            property_name = prop.fget.__name__
            try:
                for doc in await getattr(self, property_name):
                    await doc.delete()
            except DocumentDoesntExist:
                continue

    async def _delete_related(self):
        """Deletes related documents or pops field values."""

        self_properties = set({v for v in self.__class__.__dict__.values()
                               if isinstance(v, property)})

        relations = set(Document.relations).intersection(self_properties)

        await self._delete_by_prop({prop: delete_info for prop, delete_info
                                    in Document.relations.items() if prop in relations
                                    })

    async def delete(self):
        """Delete current document and related fields or documents base on related."""

        result = await self.__class__._collection().delete_one({"_id": self._id})
        await self._delete_related()
        return result

    @staticmethod
    def related(self_path, other_path, multiple=True, parent=True):
        """Decorator for related documents.

        :param parent: show relations type. When Parent updated or deleted Child is also updated
        and deleted. When Child is updated or deleted Parent stays the same.
        :param self_path: Document.key to self pk
        :param other_path: Document.key to other pk
        :param multiple: return multiple documents or only one
        """

        def func_wrapper(func):

            self_field = ".".join(self_path.split(".")[1:])
            other_field = ".".join(other_path.split(".")[1:])

            def get_other_document():
                for subclass in Document.__subclasses__():
                    if subclass.__name__ == other_path.split(".")[0]:
                        return subclass

            @wraps(func)
            async def fget(self):
                other_document = get_other_document()

                if multiple:
                    return await other_document.many(**{other_field: self[self_field]})
                else:
                    return await other_document.one(**{other_field: self[self_field]})

            result = property(fget=fget)

            delete_item = {
                "self_field": self_field,
                "other_field": other_field,
                "parent": parent,
                "other_document_func": get_other_document
            }

            Document.relations[result] = delete_item

            return result

        return func_wrapper

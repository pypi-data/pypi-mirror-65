import urllib.parse

from motor.motor_asyncio import AsyncIOMotorClient


class DatabaseClient:
    def __init__(self, uri: str = None, replica_set: list = None, host: str = None,
                 username: str = None, password: str = None, auth_database: str = "admin"):

        if uri:
            self.client = AsyncIOMotorClient(uri)
        else:
            if replica_set:
                host = ",".join(replica_set)

            if not username or not password:
                uri = f"mongodb://{host}"
            else:
                username = urllib.parse.quote_plus(username)
                password = urllib.parse.quote_plus(password)
                uri = f"mongodb://{username}:{password}@{host}/{auth_database}"

            self.client = AsyncIOMotorClient(uri)

    async def create(self, document):

        await self.client[document._database_][document._collection_].insert_one(
            document.__dict__
        )
        document._shadow_copy_ = document.__dict__.copy()

    async def update(self, document):

        await self.client[document._database_][document._collection_].update_one(
            document._shadow_copy_,
            {"$set": document.__dict__}
        )

    async def delete(self, document):

        await self.client[document._database_][document._collection_].delete_one(
            document._shadow_copy_
        )
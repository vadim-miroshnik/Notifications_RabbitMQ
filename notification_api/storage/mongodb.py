from motor.motor_asyncio import AsyncIOMotorClient

from .interface import Storage


class Mongodb(Storage):
    def __init__(self, mongodb: AsyncIOMotorClient, db: str, coll: str):
        self.mongodb = mongodb
        self.db = db
        self.coll = coll

    async def insert(self, item: dict) -> dict:
        print(self.mongodb)
        return await self.mongodb[self.db][self.coll].insert_one(item)

    async def select(self, item: dict) -> dict:
        return await self.mongodb[self.db][self.coll].find_one(item)

    async def delete(self, item: dict) -> None:
        return await self.mongodb[self.db][self.coll].delete_one(item)

    async def update(self, item: dict, prop: dict) -> bool:
        return await self.mongodb[self.db][self.coll].update_one(item, prop)

    async def select_items(self, fltr: dict, **kwargs) -> list:
        cursor = await self.mongodb[self.db][self.coll].find(fltr)
        return list(cursor)

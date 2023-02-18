from functools import lru_cache

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from services.notifications import NotificationsService
from storage.mongodb import Mongodb


mongoclient: AsyncIOMotorClient | None = None


async def get_mongodb() -> AsyncIOMotorClient:
    return mongoclient


@lru_cache()
def get_mongodb_notifications(
    client: AsyncIOMotorClient = Depends(get_mongodb),
    db: str = "movies",
    coll: str = "notifications"
) -> NotificationsService:
    mongo: Mongodb = Mongodb(client, db, coll)
    return NotificationsService(mongo)

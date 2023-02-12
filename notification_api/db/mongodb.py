from functools import lru_cache
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient
from storage.mongodb import Mongodb, get_collection
from services.notifications import NotificationsService


mongodb: AsyncIOMotorClient | None = None

# todo env variables
mongodb = AsyncIOMotorClient(
    "mongodb://mongos1:27017/?serverSelectionTimeoutMS=2000&directConnection=true&uuidRepresentation=standard"
)


@lru_cache()
def get_mongodb_notifications(mongo: AsyncIOMotorClient = Depends(get_collection(mongodb, "movies", "notifications"))
                              ) -> NotificationsService:
    return NotificationsService(mongo)



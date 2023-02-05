from motor.motor_asyncio import AsyncIOMotorClient

mongodb: AsyncIOMotorClient | None = None
mongodb = AsyncIOMotorClient(
    "mongodb://mongos1:27017/?serverSelectionTimeoutMS=2000&directConnection=true&uuidRepresentation=standard"
)

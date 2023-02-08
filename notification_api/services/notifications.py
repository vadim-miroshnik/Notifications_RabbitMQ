import uuid
from uuid import UUID

from storage.mongodb import Mongodb
from models.notification import Notification


class NotificationsService:
    def __init__(self, stor: Mongodb):
        self.stor = stor

    async def add(self, notification: Notification):
        return await self.stor.insert(
            {
                "_id": str(uuid.uuid4()),
                "subject": notification.subject,
                "template": notification.template,
                "content_data": notification.content_data,
                "recepients": notification.recepients,
                "notif_type": notification.notif_type,
                "priority": notification.priority,
            }
        )

    async def delete(self, user_id: str, movie_id: str):
        return await self.stor.update(
            {"_id": user_id}, {"$pull": {"bookmarks": movie_id}}
        )

    async def get(self, user_id: str):
        return await self.stor.select({"_id": user_id})

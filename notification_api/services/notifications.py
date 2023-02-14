import datetime

from models.notification import Notification
from storage.mongodb import Mongodb


class NotificationsService:
    def __init__(self, stor: Mongodb):
        self.stor = stor

    async def add(self, notification: Notification):
        return await self.stor.insert(notification.as_dict)

    async def get(self, id: str):
        return await self.stor.select({"_id": id})

    async def delivered(self, id: str, email: str):
        notification = await self.stor.select({"id": id})
        if notification:
            # recipient = next(r for r in notification["recipients"] if r["email"] == email)
            return await self.stor.update(
                {"id": id, "recipients.email": email},
                {"$set": {"recipients.$.delivered": datetime.datetime.now()}},
            )
        return None

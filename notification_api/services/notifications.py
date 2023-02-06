from uuid import UUID

from storage.mongodb import Mongodb


class NotificationsService:
    def __init__(self, stor: Mongodb):
        self.stor = stor

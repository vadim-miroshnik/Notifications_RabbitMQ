from enum import Enum

from pydantic import BaseModel


class NotifTypeEnum(str, Enum):
    EMAIL = "email"
    WEBSOCKET = "websocket"


class PriorityEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Recipient(BaseModel):
    email: str
    phone: str | None = None
    fullname: str | None = None
    data: dict | None = None
    timezone: int = 0


class Notification(BaseModel):
    id: str
    notif_type: NotifTypeEnum = NotifTypeEnum.EMAIL
    subject: str | None = None
    template: str | None = None
    recipients: list[Recipient] = []
    priority: PriorityEnum = PriorityEnum.LOW


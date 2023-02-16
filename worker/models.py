from enum import Enum

from pydantic import BaseModel


class NotifTypeEnum(str, Enum):
    EMAIL = "email"
    WEBSOCKET = "websocket"


class Notification(BaseModel):
    notif_type: NotifTypeEnum = NotifTypeEnum.EMAIL
    subject: str | None = None
    template: str | None = None
    content_data: list[dict] = []
    recepients: list[str] = []

from enum import Enum
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from models.notification import NotifTypeEnum, PriorityEnum

class UUIDMixin(BaseModel):
    user_id: UUID | None = None
    notif_id: UUID | None = None


class NotifResponse(UUIDMixin, BaseModel):
    text: str | None = None
    notif_dt: datetime | None = None


class NotifRequest(UUIDMixin, BaseModel):
    notif_type: NotifTypeEnum = NotifTypeEnum.EMAIL
    subject: str | None = None
    template: str | None = None
    content_data: list[str] = []
    recepients: list[str] = []
    priority: PriorityEnum = PriorityEnum.LOW

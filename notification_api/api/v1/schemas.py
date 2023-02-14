from datetime import datetime
from uuid import UUID

from models.notification import NotifTypeEnum, PriorityEnum
from pydantic import BaseModel


class UUIDMixin(BaseModel):
    user_id: UUID | None = None
    notif_id: UUID | None = None


class NotifResponse(UUIDMixin, BaseModel):
    notif_dt: datetime | None = None


class NotifRequest(UUIDMixin, BaseModel):
    notif_type: NotifTypeEnum = NotifTypeEnum.EMAIL
    subject: str | None = None
    template_id: str | None = None
    data: dict | None = None
    group_id: str | None = None
    priority: PriorityEnum = PriorityEnum.LOW


class UserRequest(BaseModel):
    login: str
    fullname: str | None = None
    password: str | None = None
    email: str
    phone: str | None = None


class UserResponse(BaseModel):
    id: str
    login: str
    fullname: str | None = None
    email: str
    phone: str | None = None
    allow_send_email: bool
    confirmed_email: bool
    created_at: datetime
    updated_at: datetime

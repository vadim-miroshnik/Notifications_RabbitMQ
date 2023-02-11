from enum import Enum
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class NotifTypeEnum(str, Enum):
    EMAIL = "email"
    PUSH = "push"
    SMS = "sms"


class PriorityEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class UUIDMixin(BaseModel):
    user_id: UUID | None = None
    notif_id: UUID | None = None


class Notification(UUIDMixin, BaseModel):
    notif_type: NotifTypeEnum = NotifTypeEnum.EMAIL
    subject: str | None = None
    template: str | None = None
    content_data: list[str] = []
    recepients: list[str] = []
    priority: PriorityEnum = PriorityEnum.LOW

    def __init__(
        self,
        template: str,
        data: list[str],
        recipients: list[str],
        type: NotifTypeEnum = NotifTypeEnum.EMAIL,
        subject: str = "Ad message",
        priority: PriorityEnum = PriorityEnum.LOW,
    ) -> None:
        super().__init__(
            notif_type=type,
            subject=subject,
            template=template,
            content_data=data,
            recepients=recipients,
            priority=priority

        )
from enum import Enum
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

# from bitly_api import Connection
# from datetime import datetime, timedelta


class NotifTypeEnum(str, Enum):
    EMAIL = "email"
    PUSH = "push"
    SMS = "sms"


class PriorityEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Recipient(BaseModel):
    email: str
    phone: str | None = None
    fullname: str | None = None
    data: dict | None = None

    def __init__(
        self,
        email: str = None,
        phone: str = None,
        fullname: str = None
    ) -> None:
        super().__init__(
            email=email,
            phone=phone,
            fullname=fullname
        )
        # shortener = Connection(access_token="1ce341a12357a2e9976b6653c84d45ee4cc64cfb")
        # url = shortener.shorten(f"http://127.0.0.1/api/v1/users/confirmed/{email}/{datetime.now() + timedelta(hours=1)}/http://0.0.0.0")
        self.data = {"url": "http://0.0.0.0"}


class Notification(BaseModel):
    id: UUID
    notif_type: NotifTypeEnum = NotifTypeEnum.EMAIL
    subject: str | None = None
    template: str | None = None
    recipients: list[Recipient] = []
    priority: PriorityEnum = PriorityEnum.LOW

    def __init__(
        self,
        id: str = None,
        template: str = "",
        recipients: list[Recipient] = [],
        type: NotifTypeEnum = NotifTypeEnum.EMAIL,
        subject: str = "Ad message",
        priority: PriorityEnum = PriorityEnum.LOW,
    ) -> None:
        super().__init__(
            id=id,
            notif_type=type,
            subject=subject,
            template=template,
            recipients=recipients,
            priority=priority
        )

    @property
    def as_dict(self) -> dict:
        return {
            id: self.id,
            'template': self.template,
            'subject': self.subject,
            'type': self.notif_type.value,
            'priority': self.priority.value,
            'recipients': [{'email': r.email, 'fullname': r.fullname, 'phone': r.phone, 'data': r.data} for r in self.recipients],
        }
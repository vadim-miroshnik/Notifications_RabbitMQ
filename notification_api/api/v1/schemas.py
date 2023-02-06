from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UUIDMixin(BaseModel):
    user_id: UUID | None = None
    notif_id: UUID | None = None


class NotifResponse(UUIDMixin, BaseModel):
    text: str | None = None
    notif_dt: datetime | None = None

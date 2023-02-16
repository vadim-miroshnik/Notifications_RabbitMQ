import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from db.postgres import Base


class Template(Base):
    __tablename__ = "template"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = Column(String, nullable=False)
    template = Column(String, nullable=True)
    type = Column(String, nullable=False)
    priority = Column(String, nullable=False)

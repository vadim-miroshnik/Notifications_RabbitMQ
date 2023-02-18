import uuid

from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID

from db.postgres import Base


class Template(Base):
    __tablename__ = "template"
    id = Column(
        Text(length=36),
        primary_key=True,
        default=str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )
    name = Column(String, nullable=False)
    template = Column(String, nullable=True)
    type = Column(String, nullable=False)
    priority = Column(String, nullable=False)

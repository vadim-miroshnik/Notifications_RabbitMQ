from db.postgres import Base
from sqlalchemy import Column, String

import uuid
from sqlalchemy.dialects.postgresql import UUID


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
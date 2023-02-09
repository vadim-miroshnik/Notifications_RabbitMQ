from db.postgres import Base
from sqlalchemy import TIMESTAMP, Column, String, Boolean
from sqlalchemy.sql import func
from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL
import uuid
from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    __tablename__ = "movies_user"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=True)
    email = Column(String)
    fullname = Column(String)
    phone = Column(String)
    subscribed = Column(Boolean)

    def __init__(self, login=None, password=None, email=None, fullname=None, phone=None, subscribed=False):
        self.login = login
        self.password = password
        self.email = email
        self.fullname = fullname
        self.phone = phone
        self.subscribed = subscribed

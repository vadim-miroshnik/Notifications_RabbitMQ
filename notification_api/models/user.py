import datetime
from db.postgres import Base
from sqlalchemy import TIMESTAMP, Column, String, Boolean, Table, ForeignKey
from sqlalchemy.sql import func
from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref


user_notification = Table(
    "UserNotificationUserGroup",
    Base.metadata,
    Column("id", primary_key=True),
    Column("user_id", ForeignKey('user.id'), primary_key=False),
    Column("notification_user_group_id", ForeignKey('notificationgroup.id'), primary_key=False)
)

class NotificationGroup(Base):
    __tablename__ = "notificationgroup"
    # __table_args__ = {"schema": "content"}
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = Column(String, nullable=False)
    #users = relationship("User", secondary=user_notification, backref='notificationgroups')


class User(Base):
    __tablename__ = "user"
    # __table_args__ = {"schema": "content"}
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
    allow_send_email = Column(Boolean)
    confirmed_email = Column(Boolean)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    '''notification_group = relationship("NotificationGroup", secondary=user_notification,
                                backref='User',
                                lazy='dynamic')'''
    groups = relationship("NotificationGroup", secondary=user_notification,
                          primaryjoin=id == user_notification.c.user_id,
                          secondaryjoin=NotificationGroup.id == user_notification.c.notification_user_group_id,
                          backref='users')

    def __init__(self, login=None, password=None, email=None, fullname=None, phone=None, subscribed=False):
        self.login = login
        self.password = password
        self.email = email
        self.fullname = fullname
        self.phone = phone
        self.allow_send_email = subscribed
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        self.confirmed_email = False

'''
class UserNotificationUserGroup(Base):
    __tablename__ = "UserNotificationUserGroup"
    # __table_args__ = {"schema": "content"}
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    notification_user_group_id = Column("notification_user_group_id", ForeignKey('user.id'))
    user_id = Column("user_id", ForeignKey('user.id'))

    def __init__(self, user_id=None, group_id=None):
        self.notification_user_group_id = group_id
        self.user_id = user_id
'''
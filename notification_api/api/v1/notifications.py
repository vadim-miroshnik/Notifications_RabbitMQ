import contextlib
import datetime
import uuid
from http import HTTPStatus
from urllib.parse import urlencode
from urllib.request import urlopen

from auth.auth_bearer import auth
from db.mongodb import get_mongodb_notifications
from db.postgres import get_db
from db.queue import get_queue_service
from fastapi import APIRouter, Body, Depends, HTTPException, Request
from models.notification import (Notification, NotifTypeEnum, PriorityEnum,
                                 Recipient)
from models.template import Template
from models.user import User, user_notification
from services.notifications import NotificationsService
from sqlalchemy.orm import Session
from storage.queue import QueueService

from .schemas import NotifRequest, NotifResponse

router = APIRouter()


@router.post(
    "/add-single",
    responses={
        int(HTTPStatus.CREATED): {
            "model": NotifResponse,
            "description": "Successful Response",
        },
    },
    summary="Создать персонализированную рассылку",
    description="Создать персонализированную рассылку",
    tags=["notifications"],
    dependencies=[Depends(auth)],
)
async def add_person_notification(
    request: Request,
    data: NotifRequest = Body(default=None),
    db: Session = Depends(get_db),
    queue: QueueService = Depends(get_queue_service),
    service: NotificationsService = Depends(get_mongodb_notifications),
) -> NotifResponse:
    user_id = request.state.user_id
    user = db.query(User).filter_by(id=data.user_id).all()[0]
    if not getattr(user, "allow_send_email"):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Пользователь не подписан на получение уведомлений",
        )
    template = db.query(Template).filter_by(id=data.template_id).all()[0]
    id = str(uuid.uuid4())
    email = getattr(user, "email")
    url = f"http://0.0.0.0:8000/api/v1/notifications/reply/{id}/{email}"
    short_url = make_tiny(url)
    notification = Notification(
        id=id,
        template=getattr(template, "template"),
        recipients=[
            Recipient(
                email=email,
                fullname=getattr(user, "fullname"),
                phone=getattr(user, "phone"),
                url=short_url,
                data=data.data,
            )
        ],
        type=getattr(template, "type"),
        subject=data.subject,
        priority=getattr(template, "priority"),
    )
    await queue.send(data.priority, "notification", notification)
    await service.add(notification)
    return NotifResponse(user_id=user_id, notif_id=id, notif_dt=datetime.datetime.now())


@router.post(
    "/add-group",
    responses={
        int(HTTPStatus.CREATED): {
            "model": NotifResponse,
            "description": "Successful Response",
        },
    },
    summary="Создать групповую рассылку",
    description="Создать групповую рассылку",
    tags=["notifications"],
    dependencies=[Depends(auth)],
)
async def add_group_notifications(
    request: Request,
    data: NotifRequest = Body(default=None),
    db: Session = Depends(get_db),
    queue: QueueService = Depends(get_queue_service),
    service: NotificationsService = Depends(get_mongodb_notifications),
) -> NotifResponse:
    user_id = request.state.user_id
    id = str(uuid.uuid4())
    template = db.query(Template).filter_by(id=data.template_id).all()[0]
    links = (
        db.query(user_notification)
        .filter_by(notification_user_group_id=data.group_id)
        .all()
    )
    recipients = []
    for l in links:
        user = db.query(User).filter_by(id=l.user_id).first()
        if getattr(user, "allow_send_email"):
            email = getattr(user, "email")
            url = f"http://0.0.0.0:8000/api/v1/notifications/reply/{id}/{email}"
            short_url = make_tiny(url)
            recipient = Recipient(
                email=email,
                fullname=getattr(user, "fullname"),
                phone=getattr(user, "phone"),
                url=short_url,
                data=data.data,
            )
            recipients.append(recipient)
    notification = Notification(
        id=id,
        template=getattr(template, "template"),
        recipients=recipients,
        type=getattr(template, "type"),
        subject=data.subject,
        priority=getattr(template, "priority"),
    )
    await queue.send(data.priority, "notification", notification)
    await service.add(notification)
    return NotifResponse(user_id=user_id, notif_id=id, notif_dt=datetime.datetime.now())


@router.get(
    "/reply/{id}/{email}",
    responses={
        int(HTTPStatus.OK): {
            "model": NotifResponse,
            "description": "Successful Response",
        },
    },
    summary="Получить ответ от пользователя",
    description="Получить ответ от пользователя",
    tags=["notifications"],
    dependencies=[Depends(auth)],
)
async def reply_from_user(
    request: Request,
    id: str,
    email: str,
    service: NotificationsService = Depends(get_mongodb_notifications),
) -> NotifResponse:
    user_id = request.state.user_id
    await service.delivered(id, email)
    return NotifResponse(user_id=user_id, notif_id=id, notif_dt=datetime.datetime.now())


def make_tiny(url):
    request_url = "http://tinyurl.com/api-create.php?" + urlencode({"url": url})
    with contextlib.closing(urlopen(request_url)) as response:
        return response.read().decode("utf-8 ")

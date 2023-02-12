import uuid
from http import HTTPStatus
from uuid import UUID

from auth.auth_bearer import auth
from bson import json_util
from fastapi import APIRouter, Body, Depends, Header, HTTPException, Query, Request
from db.mongodb import get_mongodb_notifications
from services.notifications import NotificationsService
from db.queue import get_queue_service
from storage.queue import QueueService
# from sqlalchemy.orm import sessionmaker
# from db.postgres import get_db
from .schemas import NotifResponse, NotifRequest
from models.notification import Notification

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
    # dependencies=[Depends(auth)],
)
async def add_person_notification(
    request: Request,
    data: NotifRequest = Body(default=None),
    # movie_id: UUID = Query(default=uuid.uuid4()),
    # db: sessionmaker = Depends(get_db),
    queue: QueueService = Depends(get_queue_service),
    service: NotificationsService = Depends(get_mongodb_notifications),
) -> NotifResponse:
    user = "3fa85f64-5717-4562-b3fc-2c963f66afa6"  # request.state.user_id
    await service.add(
        Notification(
            template=data.template,
            data=data.content_data,
            recipients=data.recepients,
            type=data.notif_type.value,
            subject=data.subject,
            priority=data.priority,
        )
    )
    return NotifResponse(
        user_id=user,
    )


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
    # movie_id: UUID = Query(default=uuid.uuid4()),
    queue: QueueService = Depends(get_queue_service),
    service: NotificationsService = Depends(get_mongodb_notifications),
) -> NotifResponse:
    user = request.state.user_id
    # await service.add(user, str(movie_id))
    return NotifResponse(
        user_id=user,
    )


@router.get(
    "/reply",
    responses={
        int(HTTPStatus.CREATED): {
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
    # movie_id: UUID = Query(default=uuid.uuid4()),
    service: NotificationsService = Depends(get_mongodb_notifications),
) -> NotifResponse:
    user = request.state.user_id
    # await service.add(user, str(movie_id))
    return NotifResponse(
        user_id=user,
    )

@router.get(
    "/test",
    responses={
        int(HTTPStatus.CREATED): {
            "model": NotifResponse,
            "description": "Successful Response",
        },
    },
    summary="Получить ответ от пользователя",
    description="Получить ответ от пользователя",
    tags=["notifications"],
)
async def test(
    request: Request,
    queue: QueueService = Depends(get_queue_service),
) -> NotifResponse:
    await queue.send("notif-low", "test-test", "test-test")
    return NotifResponse(
        user_id=uuid.uuid4(),
    )


@router.get(
    "/test2",
    responses={
        int(HTTPStatus.CREATED): {
            "model": NotifResponse,
            "description": "Successful Response",
        },
    },
    summary="Получить ответ от пользователя",
    description="Получить ответ от пользователя",
    tags=["notifications"],
)
async def test2(
    request: Request,
    queue: QueueService = Depends(get_queue_service),
) -> NotifResponse:
    await queue.read("notif-low")
    return NotifResponse(
        user_id=uuid.uuid4(),
    )
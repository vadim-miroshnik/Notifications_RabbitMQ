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
from sqlalchemy.orm import sessionmaker
from db.postgres import get_db
from .schemas import NotifResponse

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
    # movie_id: UUID = Query(default=uuid.uuid4()),
    db: sessionmaker = Depends(get_db),
    queue: QueueService = Depends(get_queue_service),
    service: NotificationsService = Depends(get_mongodb_notifications),
) -> NotifResponse:
    user = request.state.user_id
    # await service.add(user, str(movie_id))
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



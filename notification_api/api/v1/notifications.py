import uuid
from http import HTTPStatus
from uuid import UUID

from auth.auth_bearer import auth
from bson import json_util
from fastapi import APIRouter, Body, Depends, Header, HTTPException, Query, Request
from db.mongodb import get_mongodb_notifications
from services.notifications import NotificationsService
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
    # kafka: KafkaService = Depends(get_kafka_service),
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
    # kafka: KafkaService = Depends(get_kafka_service),
    service: NotificationsService = Depends(get_mongodb_notifications),
) -> NotifResponse:
    user = request.state.user_id
    # await service.add(user, str(movie_id))
    return NotifResponse(
        user_id=user,
    )



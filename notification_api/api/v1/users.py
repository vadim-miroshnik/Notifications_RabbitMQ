import uuid
from http import HTTPStatus
from uuid import UUID

from auth.auth_bearer import auth
from auth.auth_handler import encode_jwt
from bson import json_util
from fastapi import APIRouter, Body, Depends, Header, HTTPException, Query, Request
from db.mongodb import get_mongodb_notifications
from services.notifications import NotificationsService
from .schemas import NotifResponse

router = APIRouter()



@router.patch(
    "/enable-notifications",
    responses={
        int(HTTPStatus.CREATED): {
            "model": NotifResponse,
            "description": "Successful Response",
        },
    },
    summary="Разрешить/запретить рассылку",
    description="Разрешить/запретить рассылку",
    tags=["users"],
    dependencies=[Depends(auth)],
)
async def enable_notifications(
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


@router.get(
    "/login",
    response_model=None,
    summary="",
    description="",
    response_description="",
)
async def get_access_token(user_id: str | None = None) -> str:
    if not user_id:
        user_id = str(uuid.uuid4())
    token: str = encode_jwt(user_id)
    return token


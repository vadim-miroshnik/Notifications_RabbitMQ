import uuid
from http import HTTPStatus
from uuid import UUID

from auth.auth_bearer import auth
from auth.auth_handler import encode_jwt
from bson import json_util
from fastapi import APIRouter, Body, Depends, Header, HTTPException, Query, Request
from db.mongodb import get_mongodb_notifications
from sqlalchemy.orm import Session
from db.postgres import get_db
from services.notifications import NotificationsService
from .schemas import NotifResponse
from models.user import User

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
    db: Session = Depends(get_db),
    # movie_id: UUID = Query(default=uuid.uuid4()),
    # kafka: KafkaService = Depends(get_kafka_service),
    service: NotificationsService = Depends(get_mongodb_notifications),
) -> NotifResponse:
    test = next(db).query(User).all()
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

@router.post(
    "/register",
    responses={
        int(HTTPStatus.CREATED): {
            "model": NotifResponse,
            "description": "Successful Response",
        },
    },
    summary="Регистрация пользователя",
    description="Регистрация пользователя",
    tags=["users"],
    dependencies=[Depends(auth)],
)
async def register(
    request: Request,
    db: Session = Depends(get_db),
    service: NotificationsService = Depends(get_mongodb_notifications),
) -> NotifResponse:
    session = next(db)
    test = session.add(User(login="test", password="test", email="test@test.ru", fullname="test", phone="1234567890", subscribed=False))
    session.commit()
    return NotifResponse(
        user_id=user,
    )
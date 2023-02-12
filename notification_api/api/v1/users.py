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
from .schemas import UserResponse, UserRequest
from models.user import User

router = APIRouter()


@router.patch(
    "/enable-notifications",
    responses={
        int(HTTPStatus.CREATED): {
            "model": UserResponse,
            "description": "Successful Response",
        },
    },
    summary="Разрешить/запретить рассылку",
    description="Разрешить/запретить рассылку",
    tags=["users"],
    # dependencies=[Depends(auth)],
)
async def enable_notifications(
    request: Request,
    db: Session = Depends(get_db),
) -> UserResponse:
    user_id = "d436ed9e-cfdb-4b44-9c15-cc941dd5459e"
    # user_id = request.state.user_id
    session = list(db)[0]
    user = session.query(User).filter_by(id=user_id).all()[0]
    setattr(user, "allow_send_email", True)
    session.commit()
    return user.__dict__


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
            "model": UserResponse,
            "description": "Successful Response",
        },
    },
    summary="Регистрация пользователя",
    description="Регистрация пользователя",
    tags=["users"],
)
async def register(
    data: UserRequest = Body(default=None),
    db: Session = Depends(get_db),
    service: NotificationsService = Depends(get_mongodb_notifications),
) -> UserResponse:
    session = next(db)
    session.add(User(login=data.login, password=data.password, email=data.email, fullname=data.fullname, phone=data.phone, subscribed=False))
    session.commit()
    user = session.query(User).filter_by(login=data.login).all()[0]
    return UserResponse(
        id=str(user.id),
        login=user.login,
        fullname=user.fullname,
        email=user.email,
        phone=user.phone,
        allow_send_email=user.allow_send_email,
        confirmed_email=user.confirmed_email,
        created_at=user.created_at,
        updated_at=user.updated_at
    )

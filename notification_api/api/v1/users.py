import httpx
import datetime
import uuid
from datetime import datetime, timedelta
from http import HTTPStatus
from urllib.parse import urlencode

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse

from auth.auth_bearer import auth
from auth.auth_handler import encode_jwt
from db.postgres import get_db_service
from db.queue import get_queue_service
from models.notification import Notification, NotifTypeEnum, PriorityEnum, Recipient
from storage.queue import QueueService
from .schemas import UserRequest, UserResponse
from core.config import settings
from services.db import DBService


router = APIRouter()


@router.get(
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
    #dependencies=[Depends(auth)],
)
async def enable_notifications(
    request: Request,
    db: DBService = Depends(get_db_service),
) -> UserResponse:
    #user_id = request.state.user_id
    user_id = "96d9707e-0600-4eac-ba2a-8a1def9516ac"
    db = await db
    user = await db.update_user_prop(user_id, "allow_send_email", True)
    return UserResponse(
        id=str(user.id),
        login=user.login,
        fullname=user.fullname,
        email=user.email,
        phone=user.phone,
        allow_send_email=user.allow_send_email,
        confirmed_email=user.confirmed_email,
        created_at=user.created_at,
        updated_at=user.updated_at,
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
    db: DBService = Depends(get_db_service),
    queue: QueueService = Depends(get_queue_service),
) -> UserResponse:
    db = await db
    await db.add_user(login=data.login,
            password=data.password,
            email=data.email,
            fullname=data.fullname,
            phone=data.phone,
            subscribed=False
    )
    user = await db.get_user_by_login(data.login)
    template = await db.get_template_by_name("welcome")
    email = getattr(user, "email")
    url = f"{settings.notify_app.confirmed_url}/{email}/{datetime.now() + timedelta(hours=1)}/google.com"
    short_url = await make_tiny(url)
    notification = Notification(
        id=str(uuid.uuid4()),
        template=getattr(template, "template"),
        recipients=[
            Recipient(
                email=email,
                fullname=getattr(user, "fullname"),
                phone=getattr(user, "phone"),
                url=short_url,
            )
        ],
        type=NotifTypeEnum.EMAIL,
        subject="Welcome",
        priority=PriorityEnum.HIGH,
    )
    await queue.send(PriorityEnum.HIGH, "register", notification)
    return UserResponse(
        id=str(user.id),
        login=user.login,
        fullname=user.fullname,
        email=user.email,
        phone=user.phone,
        allow_send_email=user.allow_send_email,
        confirmed_email=user.confirmed_email,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


@router.get(
    "/confirmed/{email}/{expire_time}/{redirect_url}",
    responses={
        int(HTTPStatus.OK): {
            "model": UserResponse,
            "description": "Successful Response",
        },
    },
    summary="Подтверждение почтового адреса пользователя",
    description="Подтверждение почтового адреса пользователя",
    tags=["users"],
    dependencies=[Depends(auth)],
)
async def confirmed(
    email: str,
    expire_time: str,
    redirect_url: str,
    db: DBService = Depends(get_db_service),
) -> RedirectResponse:
    exp: datetime = datetime.strptime(expire_time, "%Y-%m-%d %H:%M:%S.%f")
    if datetime.now() > exp:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Превышено время ожидания")
    db = await db
    user = await db.get_user_by_email(email)
    user_id = getattr((user, "email"))
    await db.update_user_prop(user_id, "allow_send_email", True)
    return RedirectResponse(f"http://{redirect_url}")


async def make_tiny(url):
    request_url = "http://tinyurl.com/api-create.php?" + urlencode({"url": url})
    async with httpx.AsyncClient() as client:
        response = await client.get(request_url)
        return response.text

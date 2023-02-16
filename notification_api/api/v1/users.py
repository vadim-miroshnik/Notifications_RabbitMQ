import contextlib
import datetime
import uuid
from datetime import datetime, timedelta
from http import HTTPStatus
from urllib.parse import urlencode
from urllib.request import urlopen

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from auth.auth_bearer import auth
from auth.auth_handler import encode_jwt
from db.postgres import get_db
from db.queue import get_queue_service
from models.notification import Notification, NotifTypeEnum, PriorityEnum, Recipient
from models.template import Template
from models.user import User
from storage.queue import QueueService
from .schemas import UserRequest, UserResponse

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
    dependencies=[Depends(auth)],
)
async def enable_notifications(
    request: Request,
    db: Session = Depends(get_db),
) -> UserResponse:
    user_id = request.state.user_id
    user = db.query(User).filter_by(id=user_id).all()[0]
    setattr(user, "allow_send_email", True)
    db.commit()
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
    db: Session = Depends(get_db),
    queue: QueueService = Depends(get_queue_service),
) -> UserResponse:
    db.add(
        User(
            login=data.login,
            password=data.password,
            email=data.email,
            fullname=data.fullname,
            phone=data.phone,
            subscribed=False,
        )
    )
    db.commit()
    user = db.query(User).filter_by(login=data.login).all()[0]
    template = db.query(Template).filter_by(name="welcome").all()[0]
    email = getattr(user, "email")
    url = f"http://0.0.0.0:8000/api/v1/users/confirmed/{email}/{datetime.now() + timedelta(hours=1)}/google.com"
    short_url = make_tiny(url)
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
    db: Session = Depends(get_db),
) -> RedirectResponse:
    exp: datetime = datetime.strptime(expire_time, "%Y-%m-%d %H:%M:%S.%f")
    if datetime.now() > exp:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Превышено время ожидания")
    user = db.query(User).filter_by(email=email).all()[0]
    setattr(user, "confirmed_email", True)
    db.commit()
    return RedirectResponse(f"http://{redirect_url}")


def make_tiny(url):
    request_url = "http://tinyurl.com/api-create.php?" + urlencode({"url": url})
    with contextlib.closing(urlopen(request_url)) as response:
        return response.read().decode("utf-8 ")

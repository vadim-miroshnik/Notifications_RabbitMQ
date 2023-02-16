"""Конфигурация приложения."""
import logging
from logging import config as logging_config
from pathlib import Path

from core.logger import LOGGING
from pydantic import BaseModel, BaseSettings, Field

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class NotifyApp(BaseModel):
    jwt_secret_key: str = Field("someword")
    algorithm: str = Field("HS256")


class Mongo(BaseModel):
    host: str = Field("127.0.0.1")
    port: int = Field(27017)


class Postgres(BaseSettings):
    host: str = Field("127.0.0.1")
    port: int = Field(5432)
    db: str = Field("movies_database")
    user: str = Field("app")
    password: str = Field("123qwe")


class Rabbitmq(BaseModel):
    server: str = Field("127.0.0.1")
    port: int = Field(5672)
    user: str = Field("guest")
    password: str = Field("guest")


class Settings(BaseSettings):
    notify_app: NotifyApp = Field(NotifyApp())
    mongo: Mongo = Field(Mongo())
    postgres: Postgres = Field(Postgres())
    rabbitmq: Rabbitmq = Field(Rabbitmq())
    project_name: str = Field("notification")
    debug: bool = Field(False)

    class Config:
        env_file = BASE_DIR.joinpath(".env")
        env_nested_delimiter = "__"


settings = Settings()

if settings.debug:
    LOGGING["root"]["level"] = "DEBUG"

logging_config.dictConfig(LOGGING)

logging.debug("%s", settings.dict())

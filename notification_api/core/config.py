"""Конфигурация приложения."""
import logging
from logging import config as logging_config
from pathlib import Path

from pydantic import BaseSettings, BaseModel, Field

from core.logger import LOGGING

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class NotifyApp(BaseModel):
    jwt_secret_key: str = Field("someword")
    algorithm: str = Field("HS256")


class Mongo(BaseModel):
    host: str = Field("127.0.0.1")
    port: int = Field(27017)


class Settings(BaseSettings):
    notify_app: NotifyApp = Field(NotifyApp())
    mongo: Mongo = Field(Mongo())
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
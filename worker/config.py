from pathlib import Path
from pydantic import BaseModel, BaseSettings, Field

BASE_DIR = Path(__file__).resolve().parent.parent


class Worker(BaseModel):
    smtp_server: str = Field("127.0.0.1")
    smtp_port: int = Field(465)
    smtp_user: str = Field("user")
    smtp_password: str = Field("password")


class Rabbitmq(BaseModel):
    server: str = Field("127.0.0.1")
    port: int = Field(5672)
    user: str = Field("guest")
    password: str = Field("guest")


class Settings(BaseSettings):
    worker: Worker = Field(Worker())
    rabbitmq: Rabbitmq = Field(Rabbitmq())

    class Config:
        env_file = BASE_DIR.joinpath(".env")
        env_nested_delimiter = "__"


settings = Settings()

import logging
from pathlib import Path

from pydantic import BaseSettings, BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent.parent.parent
print(BASE_DIR.joinpath(".env"))


class Postgres(BaseModel):
    user: str
    password: str
    db: str
    host: str = Field("127.0.0.1")
    port: int = Field(5432)


class Settings(BaseSettings):
    postgres: Postgres
    project_name: str = Field("admin_panel")
    debug: bool = Field(False)
    secret_key: str = "django-insecure-0%hoizw!72v&21^0#=rwrdv!#4jb!*dsh6m=p+evrr^j-anh6$"

    class Config:
        env_file = BASE_DIR.joinpath(".env")
        env_nested_delimiter = "__"


settings = Settings()

logging.debug("%s", settings.dict())

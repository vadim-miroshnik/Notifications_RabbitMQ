from functools import lru_cache

from fastapi_utils.guid_type import setup_guids_postgresql
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import settings

POSTGRES_URL = f"postgresql://{settings.postgres.user}:{settings.postgres.password}@{settings.postgres.host}:{settings.postgres.port}/{settings.postgres.db}"

engine = create_engine(POSTGRES_URL, echo=True)

setup_guids_postgresql(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

db = SessionLocal()


@lru_cache()
def get_db():
    return db

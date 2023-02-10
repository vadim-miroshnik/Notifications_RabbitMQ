from functools import lru_cache
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import settings
from fastapi_utils.guid_type import setup_guids_postgresql

POSTGRES_URL = f"postgresql://{settings.postgres.user}:{settings.postgres.password}@{settings.postgres.host}:{settings.postgres.port}/{settings.postgres.db}"

engine = create_engine(POSTGRES_URL, echo=True)

setup_guids_postgresql(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


@lru_cache()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

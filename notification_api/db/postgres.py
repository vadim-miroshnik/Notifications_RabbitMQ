from functools import lru_cache
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from services.db import DBService
from core.config import settings

POSTGRES_URL = f"postgresql+asyncpg://{settings.postgres.user}:{settings.postgres.password}@{settings.postgres.host}:{settings.postgres.port}/{settings.postgres.db}"

engine = create_async_engine(POSTGRES_URL, echo=True)

# setup_guids_postgresql(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

Base = declarative_base()

db = SessionLocal()


@lru_cache()
async def get_db() -> AsyncSession:
    return SessionLocal()


@lru_cache()
def get_db_service() -> DBService:
    return DBService(db)

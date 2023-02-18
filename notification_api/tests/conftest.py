import sys
from pathlib import Path
from typing import Any
from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(str(Path(__file__).parent.parent.resolve()))

from models.user import User
from api.v1.users import router as users_router
from core.config import settings

BASE_DIR = Path(__file__).parent.resolve()

POSTGRES_URL = f"postgresql://{settings.postgres.user}:{settings.postgres.password}@{settings.postgres.host}:{settings.postgres.port}/{settings.postgres.db}"

engine = create_engine(POSTGRES_URL, echo=True)

SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def app() -> FastAPI:
    app = FastAPI()
    app.include_router(users_router)
    return app


@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session  # use the session in tests.
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(app: FastAPI, db_session: SessionTesting) -> Generator[TestClient, Any, None]:

    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def test_user_info(db_session):
    test_user_name = "test_user_2"
    user = User(
        login=test_user_name,
        password="password",
        email="testuser@example.com",
        fullname="fullname",
        phone="+79627950693",
    )
    db_session.add(user)
    db_session.commit()

    def inner():
        result = db_session.query(User).filter_by(login=test_user_name).all()[0]
        return result

    yield inner
    db_session.query(User).filter_by(login=test_user_name).delete()

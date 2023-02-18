import datetime
import os
import sys
import uuid
from pathlib import Path
from typing import Any
from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, Column, Text, String, Boolean, TIMESTAMP, Integer
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

sys.path.append(str(Path(__file__).parent.parent.resolve()))

from db.postgres import Base, db
from db import postgres
from api.v1.users import router as users_router
from models.user import User

BASE_DIR = Path(__file__).parent.resolve()

def start_application():
    app = FastAPI()
    app.include_router(users_router)
    return app


SQLALCHEMY_DATABASE_URL = f"sqlite:///{BASE_DIR}/test_db.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# Use connect_args parameter only with sqlite
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    Base.metadata.create_all(engine)  # Create the tables.
    _app = start_application()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    postgres.db = session
    yield session  # use the session in tests.
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(app: FastAPI, db_session: SessionTesting) -> Generator[TestClient, Any, None]:
    app.dependency_overrides[db] = db_session


    with TestClient(app) as client:
        yield client

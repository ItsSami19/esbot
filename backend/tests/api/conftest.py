import pytest
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine
from fastapi.testclient import TestClient

from app.main import app
from app.api.dependencies import get_db_session
from app import models  # ensures all models are registered


TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


def override_get_db_session():
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        yield session


app.dependency_overrides[get_db_session] = override_get_db_session


@pytest.fixture(name="client")
def client_fixture():
    SQLModel.metadata.create_all(test_engine)
    with TestClient(app) as client:
        yield client
    SQLModel.metadata.drop_all(test_engine)


@pytest.fixture(name="created_session")
def created_session_fixture(client: TestClient):
    response = client.post(
        "/api/v1/sessions",
        json={"title": "Test Session", "user_identifier": "test-user"},
    )
    assert response.status_code == 201
    return response.json()
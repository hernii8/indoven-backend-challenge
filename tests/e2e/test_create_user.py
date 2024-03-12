from fastapi.testclient import TestClient
import pytest
from src.infra.storage import Storage
from server import app, UserPayload


@pytest.fixture
def client():
    return TestClient(app)


@pytest.mark.e2e
@pytest.mark.usefixtures("reset_storage")
def test_create_user(client):
    """It should create a new user"""
    user_payload = UserPayload.model_validate(
        {
            "username": "username",
            "password": "password",
            "roles": [],
        }
    )
    response = client.post(
        "/users/",
        json=user_payload.model_dump(),
    )
    assert response.status_code == 201
    assert len(Storage().users) == 1 and Storage().users[0]["username"] == "username"


@pytest.mark.e2e
def test_role_error(client):
    """It should throw an error when trying to create an user with an unexpected role"""
    user_payload = UserPayload.model_validate(
        {
            "username": "username",
            "password": "password",
            "roles": ["wrong_role"],
        }
    )
    response = client.post(
        "/users/",
        json=user_payload.model_dump(),
    )
    assert response.status_code == 400
    assert len(Storage().users) == 0

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
    user_payload: UserPayload = {
        "id": "id",
        "username": "username",
        "password": "password",
        "roles": [],
    }
    response = client.post(
        "/users/",
        json=user_payload,
    )
    assert response.status_code == 201
    assert len(Storage().users) == 1 and Storage().users[0]["username"] == "username"

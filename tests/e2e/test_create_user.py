from fastapi.testclient import TestClient
import pytest
from src.infra.jwt.jwt import JWTToken
from src.infra.storage import Storage
from server import app
from src.routes.post.create_user import CreateUserPayload


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def admin_token() -> JWTToken:
    return JWTToken({"sub": "id", "is_admin": True})


@pytest.fixture
def not_admin_token() -> JWTToken:
    return JWTToken({"sub": "id", "is_admin": False})


@pytest.mark.e2e
@pytest.mark.usefixtures("reset_storage")
def test_create_user(client: TestClient, admin_token: JWTToken):
    """It should create a new user"""
    user_payload = CreateUserPayload.model_validate(
        {
            "username": "username",
            "password": "password",
            "roles": [],
        }
    )
    response = client.post(
        "/users/",
        headers={"Authorization": f"Bearer {admin_token.access_token}"},
        json=user_payload.model_dump(),
    )
    assert response.status_code == 201
    assert len(Storage().users) == 1 and Storage().users[0]["username"] == "username"


@pytest.mark.e2e
def test_role_error(client: TestClient, admin_token: JWTToken):
    """It should throw an error when trying to create an user with an unexpected role"""
    user_payload = CreateUserPayload.model_validate(
        {
            "username": "username",
            "password": "password",
            "roles": ["wrong_role"],
        }
    )
    response = client.post(
        "/users/",
        headers={"Authorization": f"Bearer {admin_token.access_token}"},
        json=user_payload.model_dump(),
    )
    assert response.status_code == 400
    assert len(Storage().users) == 0


@pytest.mark.e2e
def test_not_admin_creation_error(client: TestClient, not_admin_token: JWTToken):
    """It should not authorize the requests to create an user if the creator is not an admin"""
    user_payload = CreateUserPayload.model_validate(
        {
            "username": "username",
            "password": "password",
            "roles": [],
        }
    )
    response = client.post(
        "/users/",
        headers={"Authorization": f"Bearer {not_admin_token.access_token}"},
        json=user_payload.model_dump(),
    )
    assert response.status_code == 401
    assert len(Storage().users) == 0

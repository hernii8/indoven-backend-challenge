import pytest
from src.application.get.login import Login
from src.domain.user.errors.incorrect_password_error import IncorrectPasswordError
from src.infra.memory_repositories.memory_user_repo import MemoryUserRepo
from src.infra.crypto.hasher import Hasher
from src.infra.storage import Storage


@pytest.fixture
def loaded_repo() -> MemoryUserRepo:
    return MemoryUserRepo(
        Storage(
            users=[
                {
                    "id": "id",
                    "username": "username",
                    "password": Hasher.hash("password"),
                    "roles": [],
                },
            ]
        )
    )


@pytest.mark.usefixtures("reset_storage")
def test_login(loaded_repo):
    """It should return the corresponding user from storage"""
    logged_user = Login(user_repo=loaded_repo).execute("username", "password")
    assert logged_user.id == "id"
    assert logged_user.username == "username"


@pytest.mark.usefixtures("reset_storage")
def test_login_with_wrong_password(loaded_repo):
    """It should throw an error if the password is wrong"""
    with pytest.raises(IncorrectPasswordError):
        Login(user_repo=loaded_repo).execute("username", "wrong")

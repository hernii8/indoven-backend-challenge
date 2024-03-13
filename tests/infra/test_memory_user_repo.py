from typing import List
import pytest
from src.infra.storage import Storage
from src.domain.user.errors.user_not_found_error import UserNotFoundError
from src.infra.memory_repositories.memory_user_repo import MemoryUserRepo, UserModel


@pytest.fixture
def empty_repository() -> MemoryUserRepo:
    return MemoryUserRepo(connection=Storage())


@pytest.fixture
def loaded_repository() -> MemoryUserRepo:
    storage_users: List[UserModel] = [
        {
            "id": "id",
            "username": "username",
            "password": "password",
            "roles": [],
        },
        {
            "id": "id_2",
            "username": "username_2",
            "password": "password_2",
            "roles": [],
        },
        {
            "id": "id_3",
            "username": "username_3",
            "password": "password_3",
            "roles": [],
        },
    ]
    return MemoryUserRepo(connection=Storage(users=storage_users))


@pytest.mark.usefixtures("reset_storage")
def test_save(empty_repository):
    """It should save an user"""
    storage_user = {
        "id": "id",
        "username": "username",
        "password": "password",
        "roles": [],
    }
    user = empty_repository._to_user(storage_user)
    empty_repository.save(user)
    assert len(Storage().users) == 1 and Storage().users[0] == storage_user


@pytest.mark.usefixtures("reset_storage")
def test_get(loaded_repository):
    """It should get the user with the corresponding id"""
    first_id = Storage().users[0]["id"]
    user = loaded_repository.get(first_id)
    expected_user = loaded_repository._to_user(Storage().users[0])
    assert user == expected_user


def test_not_found(empty_repository):
    """It should raise an exception if the user cannot be found"""
    with pytest.raises(UserNotFoundError):
        empty_repository.get("anything")

import pytest
from src.infra.storage import Storage
from src.domain.not_found_error import NotFoundError
from src.domain.user import User
from src.infra.memory_user_repo import MemoryUserRepo, UserModel


@pytest.fixture
def empty_repository():
    return MemoryUserRepo(connection=Storage())


@pytest.fixture
def loaded_repository():
    storage_users: UserModel = [
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
            "roles": ["admin"],
        },
        {
            "id": "id_3",
            "username": "username_3",
            "password": "password_3",
            "roles": [],
        },
    ]
    return MemoryUserRepo(connection=Storage(users=storage_users))


def test_save(empty_repository):
    """It should save an user"""
    storage_user: UserModel = {
        "id": "id",
        "username": "username",
        "password": "password",
        "roles": [],
    }
    user = User(**storage_user)
    empty_repository.save(user)
    assert len(Storage().users) == 1 and Storage().users[0] == storage_user


def test_get(loaded_repository):
    """It should get the user with the corresponding id"""
    first_id = Storage().users[0]["id"]
    user = loaded_repository.get(first_id)
    expected_user = User(**Storage().users[0])
    assert user == expected_user


def test_not_found(empty_repository):
    """It should raise an exception if the user cannot be found"""
    with pytest.raises(NotFoundError):
        empty_repository.get("anything")

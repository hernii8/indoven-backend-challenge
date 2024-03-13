import pytest
from src.domain.entities.user import Roles, User
from src.domain.errors.invalid_password_error import InvalidPasswordError
from src.domain.errors.invalid_username_error import InvalidUsernameError
from src.domain.errors.role_not_found_error import RoleNotFoundError


def test_is_admin():
    """It should return true if the user is admin, and false otherwise"""
    admin_user = User(
        id="id", username="username", password="password", roles=[Roles.ADMIN]
    )
    not_admin_user = User(id="id", username="username", password="password", roles=[])
    assert admin_user.is_admin is True
    assert not_admin_user.is_admin is False


def test_password_validator():
    """It should throw an error if the password does not have 8 characters"""
    with pytest.raises(InvalidPasswordError):
        User(id="id", username="username", password="p", roles=[])


def test_roles_validator():
    """It should throw an error if any role is invalid"""
    with pytest.raises(RoleNotFoundError):
        User(
            id="id",
            username="username",
            password="password",
            roles=["invalid"],
        )


def test_username_validator():
    """It should throw an error if the username has invalid characters"""
    with pytest.raises(InvalidUsernameError):
        User(
            id="id",
            username="^username$",
            password="password",
            roles=[],
        )

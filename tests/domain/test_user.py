import pytest
from src.domain.user.user import User
from src.domain.user.errors.invalid_password_error import InvalidPasswordError
from src.domain.user.errors.invalid_username_error import InvalidUsernameError
from src.domain.user.errors.role_not_found_error import RoleNotFoundError
from src.domain.user.roles import Roles


def test_is_admin():
    """It should return true if the user is admin, and false otherwise"""
    admin_user = User(username="username", roles=[Roles.ADMIN]).with_hashed_password(
        "password"
    )
    not_admin_user = User(username="username", roles=[]).with_hashed_password(
        "password"
    )
    assert admin_user.is_admin is True
    assert not_admin_user.is_admin is False


def test_password_validator():
    """It should throw an error if the password does not have 8 characters"""
    with pytest.raises(InvalidPasswordError):
        User(username="username", roles=[]).with_plain_password("p")


def test_roles_validator():
    """It should throw an error if any role is invalid"""
    with pytest.raises(RoleNotFoundError):
        User(
            username="username",
            roles=["invalid"],
        )


def test_username_validator():
    """It should throw an error if the username has invalid characters"""
    with pytest.raises(InvalidUsernameError):
        User(
            username="^username$",
            roles=[],
        )

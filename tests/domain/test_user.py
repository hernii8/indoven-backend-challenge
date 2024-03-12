from src.domain.user import Roles, User


def test_is_admin():
    """It should return true if the user is admin, and false otherwise"""
    admin_user = User(
        id="id", username="username", password="password", roles=[Roles.ADMIN]
    )
    not_admin_user = User(id="id", username="username", password="password", roles=[])
    assert admin_user.is_admin is True
    assert not_admin_user.is_admin is False

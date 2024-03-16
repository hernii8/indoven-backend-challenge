from __future__ import annotations
import re
from typing import List
from uuid import uuid4
from src.domain.user.errors.invalid_password_error import InvalidPasswordError
from src.domain.user.errors.invalid_username_error import InvalidUsernameError
from src.domain.user.roles import Roles
from src.infra.shared.hasher import Hasher
from utils.type_guards import is_role_list, is_str_list


class User:
    __id: str
    __password: str
    __username: str
    __roles: List[Roles]

    def __init__(
        self,
        username: str,
        roles: List[Roles] | List[str],
        id: str | None = None,
    ):
        self.id = id
        self.username = username
        self.roles = roles

    @property
    def is_admin(self) -> bool:
        return Roles.ADMIN in self.roles

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id: str | None):
        self.__id = id or str(uuid4())

    @property
    def password(self):
        return self.__password

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, username: str):
        if not re.match(r"[a-zA-Z0-9]+", username):
            raise InvalidUsernameError
        self.__username = username

    @property
    def roles(self):
        return self.__roles

    @roles.setter
    def roles(self, roles: List[Roles] | list[str]):
        if is_str_list(roles):
            self.__roles = [Roles.from_str(role) for role in roles]
        elif is_role_list(roles):
            self.__roles = roles

    def __eq__(self, other: object) -> bool:
        if not hasattr(other, "id"):
            return False
        return other.id == self.id

    def with_plain_password(self, password: str) -> User:
        if len(password) < 8:
            raise InvalidPasswordError
        self.__password = Hasher.hash(password)
        return self

    def with_hashed_password(self, password: str) -> User:
        self.__password = password
        return self

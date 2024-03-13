from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import re
from typing import List
from uuid import uuid4
from src.domain.errors.invalid_password_error import InvalidPasswordError
from src.domain.errors.invalid_username_error import InvalidUsernameError
from src.domain.errors.role_not_found_error import RoleNotFoundError
from utils.type_guards import is_role_list, is_str_list


class Roles(Enum):
    ADMIN = "admin"

    @classmethod
    def from_str(cls, value: str) -> Roles:
        try:
            return Roles[value]
        except KeyError:
            raise RoleNotFoundError


@dataclass()
class User:
    id: str
    password: str
    username: str
    roles: List[Roles]

    @property
    def is_admin(self) -> bool:
        return Roles.ADMIN in self.roles

    def __init__(
        self,
        username: str,
        password: str,
        roles: List[Roles] | List[str],
        id: str | None = None,
    ):
        self.id = id or str(uuid4())

        if len(password) < 8:
            raise InvalidPasswordError
        self.password = password

        if not re.match(r"[a-zA-Z0-9]+", username):
            raise InvalidUsernameError
        self.username = username

        if is_str_list(roles):
            self.roles = [Roles.from_str(role) for role in roles]
        elif is_role_list(roles):
            self.roles = roles

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
import re
from typing import List
from uuid import uuid4
from src.domain.errors.invalid_password_error import InvalidPasswordError
from src.domain.errors.invalid_username_error import InvalidUsernameError
from src.domain.errors.role_not_found_error import RoleNotFoundError


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
    username: str
    password: str
    id: str = field(default_factory=lambda: str(uuid4()))
    roles: List[Roles] | List[str] = field(default_factory=lambda: [])

    @property
    def is_admin(self) -> bool:
        return Roles.ADMIN in self.roles

    def __post_init__(self):
        if len(self.password) < 8:
            raise InvalidPasswordError
        if all(isinstance(role, str) for role in self.roles):
            self.roles = [Roles.from_str(role) for role in self.roles]
        if not re.match(r"[a-zA-Z0-9]+", self.username):
            raise InvalidUsernameError

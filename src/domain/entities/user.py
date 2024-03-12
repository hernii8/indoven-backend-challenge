from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import List
from uuid import uuid4
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
    roles: List[Roles] = field(default_factory=lambda: [])

    @property
    def is_admin(self) -> bool:
        return Roles.ADMIN in self.roles

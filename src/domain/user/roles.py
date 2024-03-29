from __future__ import annotations
from enum import Enum
from src.domain.user.errors.role_not_found_error import RoleNotFoundError


class Roles(Enum):
    ADMIN = "admin"

    @classmethod
    def from_str(cls, value: str) -> Roles:
        try:
            return Roles(value)
        except ValueError:
            raise RoleNotFoundError

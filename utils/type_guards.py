from typing import Any, TypeGuard

from src.domain.entities.user import Roles


def is_str_list(val: list[Any]) -> TypeGuard[list[str]]:
    """Determines whether all objects in the list are strings"""
    return all(isinstance(x, str) for x in val)


def is_role_list(val: list[Any]) -> TypeGuard[list[Roles]]:
    """Determines whether all objects in the list are of type Roles"""
    return all(isinstance(x, Roles) for x in val)

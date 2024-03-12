from dataclasses import dataclass, field
from enum import Enum
from typing import List
from uuid import uuid4


class Roles(Enum):
    ADMIN = "admin"


@dataclass()
class User:
    username: str
    password: str
    roles: List[Roles] = field(default_factory=lambda: [])
    id: str = field(default_factory=lambda: str(uuid4()))

    @property
    def is_admin(self) -> bool:
        return Roles.ADMIN in self.roles

from dataclasses import dataclass
from enum import Enum
from typing import List


class Roles(Enum):
    ADMIN = "admin"


@dataclass()
class User:
    id: str
    username: str
    password: str
    roles: List[Roles]

    @property
    def is_admin(self):
        return Roles.ADMIN in self.roles

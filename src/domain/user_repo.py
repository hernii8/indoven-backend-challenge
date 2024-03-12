from typing import Protocol
from src.domain.user import User


class UserRepository(Protocol):
    def save(self, user: User) -> None:
        pass

    def get(self, id: str) -> User:
        pass

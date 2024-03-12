from dataclasses import dataclass, field
from typing import List, TypedDict
from src.domain.not_found_error import NotFoundError
from src.domain.user import User


class UserModel(TypedDict):
    id: str
    username: str
    password: str
    roles: List[str]


@dataclass()
class MemoryUserRepo:
    users: List[UserModel] = field(default_factory=lambda: [])

    def save(self, user: User) -> None:
        self.users.append(self.__to_storage(user))

    def get(self, id: str) -> User:
        try:
            result = next((user for user in self.users if user["id"] == id))
        except StopIteration:
            raise NotFoundError

        return self.__to_user(result)

    def __to_storage(self, user: User):
        return {
            "id": user.id,
            "username": user.username,
            "password": user.password,
            "roles": user.roles,
        }

    def __to_user(self, storage_user: UserModel):
        return User(**storage_user)

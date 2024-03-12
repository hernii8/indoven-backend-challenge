from dataclasses import dataclass
from src.infra.storage import Storage, UserModel
from src.domain.not_found_error import NotFoundError
from src.domain.user import User


@dataclass()
class MemoryUserRepo:
    connection: Storage

    def save(self, user: User) -> None:
        self.connection.users.append(self.__to_storage(user))

    def get(self, id: str) -> User:
        try:
            result = next((user for user in self.connection.users if user["id"] == id))
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

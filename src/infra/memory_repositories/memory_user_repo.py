from dataclasses import dataclass
from src.infra.storage import Storage, UserModel
from src.domain.user.errors.user_not_found_error import UserNotFoundError
from src.domain.user.user import User


@dataclass()
class MemoryUserRepo:
    connection: Storage

    def save(self, user: User) -> None:
        self.connection.users.append(self._to_storage(user))

    def get(self, id: str) -> User:
        try:
            result = next((user for user in self.connection.users if user["id"] == id))
        except StopIteration:
            raise UserNotFoundError

        return self._to_user(result)

    def _to_storage(self, user: User) -> UserModel:
        return {
            "id": user.id,
            "username": user.username,
            "password": user.password,
            "roles": [role.value for role in user.roles],
        }

    def _to_user(self, storage_user: UserModel) -> User:
        return User(**storage_user)

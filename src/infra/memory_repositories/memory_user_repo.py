from dataclasses import dataclass
from src.infra.storage import Storage, UserModel
from src.domain.errors.not_found_error import NotFoundError
from src.domain.entities.user import Roles, User


@dataclass()
class MemoryUserRepo:
    connection: Storage

    def save(self, user: User) -> None:
        self.connection.users.append(self._to_storage(user))

    def get(self, id: str) -> User:
        try:
            result = next((user for user in self.connection.users if user["id"] == id))
        except StopIteration:
            raise NotFoundError

        return self._to_user(result)

    def _to_storage(self, user: User):
        return {
            "id": user.id,
            "username": user.username,
            "password": user.password,
            "roles": user.roles,
        }

    def _to_user(self, storage_user: UserModel):
        return User(
            id=storage_user["id"],
            password=storage_user["password"],
            username=storage_user["username"],
            roles=[Roles.from_str(role) for role in storage_user["roles"]],
        )

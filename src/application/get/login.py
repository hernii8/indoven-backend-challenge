from dataclasses import dataclass
from src.domain.user.errors.incorrect_password_error import IncorrectPasswordError
from src.domain.user.user import User
from src.domain.user.user_repo import UserRepository
from src.infra.crypto.hasher import Hasher


@dataclass()
class Login:
    user_repo: UserRepository

    def execute(self, username: str, password: str) -> User:
        user = self.user_repo.get_by_username(username)
        if not Hasher.verify(password, user.password):
            raise IncorrectPasswordError
        return user

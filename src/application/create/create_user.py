from dataclasses import dataclass
from src.domain.user.errors.unauthorized_error import UnauthorizedError
from src.domain.user.user_repo import UserRepository
from src.domain.user.user import User


@dataclass(frozen=True)
class CreateUser:
    repo: UserRepository
    user: User

    def execute(self, is_admin: bool) -> None:
        if not is_admin:
            raise UnauthorizedError
        self.repo.save(self.user)

from dataclasses import dataclass
from src.domain.user.user_repo import UserRepository
from src.domain.user.user import User


@dataclass(frozen=True)
class CreateUser:
    repo: UserRepository
    user: User

    def execute(self) -> None:
        self.repo.save(self.user)

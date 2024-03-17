import os
from uuid import uuid4
from fastapi.security import OAuth2PasswordBearer
from src.infra.memory_repositories.memory_ecg_repo import MemoryECGRepository
from src.infra.memory_repositories.memory_user_repo import MemoryUserRepo
from src.infra.shared.hasher import Hasher
from src.infra.storage import Storage

ENV = os.environ.get("ENV")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="jwt")
if ENV == "test":
    user_repo = MemoryUserRepo(Storage())
else:
    user_repo = MemoryUserRepo(
        Storage(
            users=[
                {
                    "id": str(uuid4()),
                    "username": "user",
                    "password": Hasher.hash("password"),
                    "roles": [],
                },
                {
                    "id": str(uuid4()),
                    "username": "admin",
                    "password": Hasher.hash("password"),
                    "roles": ["admin"],
                },
            ]
        )
    )

ecg_repo = MemoryECGRepository(Storage())

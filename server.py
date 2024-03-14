from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from src.infra.memory_repositories.memory_ecg_repo import MemoryECGRepository
from src.infra.memory_repositories.memory_user_repo import MemoryUserRepo
from src.infra.shared.hasher import Hasher
from src.infra.storage import Storage

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="jwt")
user_repo = MemoryUserRepo(
    Storage(
        users=[
            {"username": "username", "password": Hasher.hash("password"), "roles": []},
            {
                "username": "admin",
                "password": Hasher.hash("adminpass"),
                "roles": ["admin"],
            },
        ]
    )
)
ecg_repo = MemoryECGRepository(Storage())

app = FastAPI()

from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from src.application.create_user import CreateUser
from src.domain.user import User
from src.infra.memory_user_repo import MemoryUserRepo
from src.infra.storage import Storage


app = FastAPI()
user_repo = MemoryUserRepo(Storage())


class UserPayload(BaseModel):
    username: str
    password: str
    roles: List[str]


@app.post("/users", status_code=201)
def create_user(user_payload: UserPayload):
    CreateUser(repo=user_repo, user=User(**user_payload.model_dump())).execute()

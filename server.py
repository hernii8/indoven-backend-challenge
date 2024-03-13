from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.domain.errors.role_not_found_error import RoleNotFoundError
from src.application.create.create_user import CreateUser
from src.domain.entities.user import Roles, User
from src.infra.memory_repositories.memory_user_repo import MemoryUserRepo
from src.infra.storage import Storage


app = FastAPI()
user_repo = MemoryUserRepo(Storage())


class UserPayload(BaseModel):
    username: str
    password: str
    roles: List[str]


@app.post("/users", status_code=201)
def create_user(user_payload: UserPayload):
    try:
        user_to_create = User(**user_payload.model_dump())
        CreateUser(repo=user_repo, user=user_to_create).execute()
    except RoleNotFoundError:
        raise HTTPException(status_code=400, detail="The role added is not valid.")

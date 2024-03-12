from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.domain.role_not_found_error import RoleNotFoundError
from src.application.create_user import CreateUser
from src.domain.user import Roles, User
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
    try:
        user_payload_asdict = user_payload.model_dump()
        user_to_create = User(
            username=user_payload_asdict["username"],
            password=user_payload_asdict["username"],
            roles=[Roles.from_str(role) for role in user_payload_asdict["roles"]],
        )
        CreateUser(repo=user_repo, user=user_to_create).execute()
    except RoleNotFoundError:
        raise HTTPException(status_code=400, detail="The role added is not valid.")

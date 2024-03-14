from typing import Annotated, List
from fastapi import Depends, HTTPException
from pydantic import BaseModel
from server import app, oauth2_scheme, user_repo
import jwt
from src.application.create.create_user import CreateUser
from src.domain.user.errors.role_not_found_error import RoleNotFoundError
from src.domain.user.user import User
from src.infra.shared.jwt import JWTToken


class CreateUserPayload(BaseModel):
    username: str
    password: str
    roles: List[str]


@app.post("/users", status_code=201)
def create_user(
    user_payload: CreateUserPayload, token: Annotated[str, Depends(oauth2_scheme)]
):
    try:
        payload = JWTToken.decrypt(token)
    except jwt.DecodeError:
        raise HTTPException(status_code=400, detail="Invalid token")
    if not payload.get("is_admin"):
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        user_to_create = User(**user_payload.model_dump())
        CreateUser(repo=user_repo, user=user_to_create).execute()
    except RoleNotFoundError:
        raise HTTPException(status_code=400, detail="The role added is not valid")

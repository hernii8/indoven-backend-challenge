from typing import List
from fastapi import Depends, HTTPException
from pydantic import BaseModel
from src.routes.dependencies import user_repo
from src.application.create.create_user import CreateUser
from src.domain.user.errors.role_not_found_error import RoleNotFoundError
from src.domain.user.user import User
from src.routes.middlewares.token_validator import validate_token
from src.routes.post.login import TokenContent
from fastapi import APIRouter

router = APIRouter()


class CreateUserPayload(BaseModel):
    username: str
    password: str
    roles: List[str]


@router.post("/users", status_code=201)
def create_user(
    user_payload: CreateUserPayload,
    token_content: TokenContent = Depends(validate_token),
):
    if not token_content["is_admin"]:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        user_to_create = User(**user_payload.model_dump())
        CreateUser(repo=user_repo, user=user_to_create).execute()
    except RoleNotFoundError:
        raise HTTPException(status_code=400, detail="The role added is not valid")

from typing import List
from fastapi import Depends, HTTPException
from pydantic import BaseModel
from src.domain.user.errors.invalid_password_error import InvalidPasswordError
from src.domain.user.errors.invalid_username_error import InvalidUsernameError
from src.domain.user.errors.unauthorized_error import UnauthorizedError
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


@router.post(
    "/users",
    status_code=201,
    responses={
        400: {"description": "Role, username or password not valid"},
        401: {"description": "Unauthorized"},
    },
)
def create_user(
    user_payload: CreateUserPayload,
    token_content: TokenContent = Depends(validate_token),
):
    """Create an User"""
    try:
        user_to_create = User(
            username=user_payload.username, roles=user_payload.roles
        ).with_plain_password(user_payload.password)
        CreateUser(repo=user_repo, user=user_to_create).execute(
            is_admin=token_content["is_admin"]
        )
    except RoleNotFoundError:
        raise HTTPException(status_code=400, detail="The role is not valid")
    except InvalidUsernameError:
        raise HTTPException(status_code=400, detail="The username is not valid")
    except InvalidPasswordError:
        raise HTTPException(status_code=400, detail="The password is not valid")
    except UnauthorizedError:
        raise HTTPException(status_code=401, detail="Unauthorized")
